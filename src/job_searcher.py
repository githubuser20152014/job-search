import requests
import pandas as pd
from datetime import datetime
import time
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import quote
from config import COMPANIES, KEYWORDS

class JobSearcher:
    def __init__(self):
        self.jobs = []
        
    def search_linkedin_jobs(self):
        """
        Search LinkedIn Jobs using their public RSS feeds
        """
        try:
            for company in COMPANIES:
                for keyword in KEYWORDS:
                    # Encode the search query
                    query = quote(f"{keyword} {company}")
                    
                    # LinkedIn jobs RSS feed URL
                    url = f"https://www.linkedin.com/jobs/search?keywords={query}&location=United%20States&f_C={company}"
                    print(f"Searching LinkedIn for {keyword} at {company}...")
                    
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
                                    
                                    job_data = {
                                        'source': 'LinkedIn',
                                        'company': company_name,
                                        'title': title,
                                        'link': link,
                                        'location': location,
                                        'date_found': datetime.now().strftime("%Y-%m-%d")
                                    }
                                    self.jobs.append(job_data)
                                    print(f"Found: {title} at {company_name}")
                                
                                except Exception as e:
                                    print(f"Error processing job listing: {str(e)}")
                                    continue
                        else:
                            print(f"Failed to get data. Status code: {response.status_code}")
                            
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed: {str(e)}")
                        
                    time.sleep(2)  # Be nice to LinkedIn's servers
                    
        except Exception as e:
            print(f"Error searching LinkedIn: {str(e)}")
            raise  # This will show the full error traceback

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
        """Export results to Excel"""
        if not self.jobs:
            print("No jobs found to export")
            return
            
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"\nResults exported to {filename} with {len(self.jobs)} jobs") 