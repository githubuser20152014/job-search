import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import quote
from config import KEYWORDS
import os
import openpyxl

class JobSearcher:
    def __init__(self, days_back=30):
        self.jobs = []
        # Calculate the cutoff date based on days_back parameter
        self.cutoff_date = datetime.now() - timedelta(days=days_back)
        self.days_back = days_back
        
    def is_recent_job(self, posting_date):
        """Check if job was posted within specified days"""
        try:
            if posting_date == 'Not specified':
                return False
            job_date = datetime.strptime(posting_date, '%Y-%m-%d')
            return job_date >= self.cutoff_date
        except Exception as e:
            print(f"Error parsing date {posting_date}: {str(e)}")
            return False
        
    def check_visa_requirements(self, description_text):
        """Check for visa requirement mentions in job description"""
        visa_keywords = [
            'visa', 'sponsorship', 'work authorization', 'legally authorized',
            'permanent resident', 'green card', 'citizenship', 'work permit',
            'H1B', 'H-1B', 'H1-B', 'eligible to work', 'right to work'
        ]
        
        found_terms = []
        description_lower = description_text.lower()
        
        for keyword in visa_keywords:
            if keyword in description_lower:
                # Get the surrounding context (100 characters)
                index = description_lower.find(keyword)
                start = max(0, index - 50)
                end = min(len(description_text), index + 50)
                context = description_text[start:end].strip()
                found_terms.append(context)
        
        return '; '.join(found_terms) if found_terms else 'Not mentioned'

    def search_linkedin_jobs(self):
        """
        Search LinkedIn Jobs using their public RSS feeds
        """
        try:
            for keyword in KEYWORDS:
                # Adjust LinkedIn's time filter based on days_back
                time_filter = f"&f_TPR=r{self.days_back * 86400}"  # Convert days to seconds
                query = quote(keyword)
                url = f"https://www.linkedin.com/jobs/search?keywords={query}&location=United%20States{time_filter}"
                print(f"\nSearching LinkedIn for {keyword}...")
                
                try:
                    response = requests.get(url)
                    print(f"Response status: {response.status_code}")
                    print(f"URL accessed: {url}")
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        job_cards = soup.find_all('div', class_='job-search-card')
                        
                        print(f"Found {len(job_cards)} job cards")
                        
                        for job in job_cards:
                            try:
                                title = job.find('h3', class_='base-search-card__title').text.strip()
                                company_name = job.find('h4', class_='base-search-card__subtitle').text.strip()
                                link = job.find('a', class_='base-card__full-link').get('href')
                                location = job.find('span', class_='job-search-card__location').text.strip()
                                
                                # Get job description
                                try:
                                    job_response = requests.get(link)
                                    if job_response.status_code == 200:
                                        job_soup = BeautifulSoup(job_response.text, 'html.parser')
                                        description = job_soup.find('div', class_='description__text')
                                        description_text = description.text.strip() if description else ''
                                        visa_info = self.check_visa_requirements(description_text)
                                    else:
                                        visa_info = 'Failed to fetch description'
                                except Exception as e:
                                    print(f"Error fetching job description: {str(e)}")
                                    visa_info = 'Error fetching description'
                                
                                # Get posting date
                                posting_date = job.find('time', class_='job-search-card__listdate')
                                if posting_date:
                                    posting_date = posting_date.get('datetime', '').split('T')[0]
                                else:
                                    posting_date = 'Not specified'
                                
                                # Only add job if it's recent
                                if self.is_recent_job(posting_date):
                                    job_data = {
                                        'source': 'LinkedIn',
                                        'company': company_name,
                                        'title': title,
                                        'link': link,
                                        'location': location,
                                        'posting_date': posting_date,
                                        'visa_info': visa_info,
                                        'date_found': datetime.now().strftime("%Y-%m-%d")
                                    }
                                    self.jobs.append(job_data)
                                    print(f"Found recent job: {title} at {company_name} (Posted: {posting_date})")
                                    print(f"Visa info: {visa_info}")
                                else:
                                    print(f"Skipping older job: {title} (Posted: {posting_date})")
                            
                            except Exception as e:
                                print(f"Error processing job listing: {str(e)}")
                                continue
                    else:
                        print(f"Failed to get data. Status code: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {str(e)}")
                    
                time.sleep(2)
                    
        except Exception as e:
            print(f"Error searching LinkedIn: {str(e)}")
            raise

    def search_company_careers(self):
        """
        Direct career page searches for specific companies
        """
        career_pages = {
            'Microsoft': 'https://careers.microsoft.com/us/en/search-results',
            'Google': 'https://careers.google.com/jobs/results/',
            'Meta': 'https://www.metacareers.com/jobs/',
            'IBM': 'https://careers.ibm.com/job/search'
        }
        
        # Implementation for direct career page searching
        # Note: This would need company-specific implementations
        pass

    def export_to_excel(self, filename="job_listings.xlsx"):
        """Export results to Excel with clickable links in a new timestamped worksheet"""
        if not self.jobs:
            print("No jobs found to export")
            return
        
        # Create timestamp for sheet name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        sheet_name = f'Jobs_{timestamp}'
        
        df = pd.DataFrame(self.jobs)
        
        try:
            # Use openpyxl engine for appending
            if os.path.exists(filename):
                with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
                    
                    # Auto-adjust columns' width
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                        
                        # Make links clickable
                        if column[0].value == 'link':
                            for cell in column[1:]:  # Skip header
                                if cell.value:
                                    cell.hyperlink = cell.value
                                    cell.style = 'Hyperlink'
            else:
                # Create new file
                df.to_excel(filename, index=False, sheet_name=sheet_name, engine='openpyxl')
                
                # Format the new file
                wb = pd.ExcelWriter(filename, engine='openpyxl')
                wb.book = openpyxl.load_workbook(filename)
                wb.sheets = dict((ws.title, ws) for ws in wb.book.worksheets)
                
                worksheet = wb.book[sheet_name]
                
                # Auto-adjust columns' width
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
                    # Make links clickable
                    if column[0].value == 'link':
                        for cell in column[1:]:  # Skip header
                            if cell.value:
                                cell.hyperlink = cell.value
                                cell.style = 'Hyperlink'
                
                wb.book.save(filename)
                
            print(f"\nResults exported to sheet '{sheet_name}' in {filename} with {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}") 