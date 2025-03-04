import requests
import pandas as pd
from datetime import datetime
import time
from config import APIS, KEYWORDS, COMPANIES

class JobAPIScraper:
    def __init__(self):
        self.jobs = []
        
    def search_linkedin(self):
        """
        Search LinkedIn Jobs API
        Note: Requires LinkedIn Developer Account and OAuth 2.0 setup
        """
        try:
            # Example LinkedIn API call
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            
            for keyword in KEYWORDS:
                params = {
                    'keywords': keyword,
                    'companies': COMPANIES,
                    'count': 100
                }
                
                response = requests.get(
                    APIS['LinkedIn']['base_url'],
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    jobs = response.json()
                    for job in jobs['elements']:
                        self.add_job('LinkedIn', job)
                        
        except Exception as e:
            print(f"Error with LinkedIn API: {str(e)}")

    def search_indeed(self):
        """
        Search Indeed Jobs API
        Note: Requires Indeed Publisher Account
        """
        try:
            for keyword in KEYWORDS:
                for company in COMPANIES:
                    params = {
                        'publisher': APIS['Indeed']['publisher_id'],
                        'q': keyword,
                        'company': company,
                        'format': 'json',
                        'v': '2',
                        'limit': 100
                    }
                    
                    response = requests.get(
                        APIS['Indeed']['base_url'],
                        params=params
                    )
                    
                    if response.status_code == 200:
                        jobs = response.json()
                        for job in jobs['results']:
                            self.add_job('Indeed', job)
                            
                    time.sleep(1)  # Rate limiting
                    
        except Exception as e:
            print(f"Error with Indeed API: {str(e)}")

    def search_glassdoor(self):
        """
        Search Glassdoor Jobs API
        Note: Requires Glassdoor Partner Account
        """
        try:
            for keyword in KEYWORDS:
                params = {
                    'v': '1',
                    't.p': APIS['Glassdoor']['partner_id'],
                    't.k': APIS['Glassdoor']['key'],
                    'userip': '0.0.0.0',
                    'useragent': '',
                    'action': 'jobs-prog',
                    'q': keyword,
                    'format': 'json'
                }
                
                response = requests.get(
                    APIS['Glassdoor']['base_url'],
                    params=params
                )
                
                if response.status_code == 200:
                    jobs = response.json()
                    for job in jobs['response']['jobs']:
                        if any(company.lower() in job['employer'].lower() for company in COMPANIES):
                            self.add_job('Glassdoor', job)
                            
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            print(f"Error with Glassdoor API: {str(e)}")

    def add_job(self, source, job_data):
        """Process and add job to the list based on the source"""
        try:
            if source == 'LinkedIn':
                job = {
                    'source': source,
                    'company': job_data.get('company', {}).get('name', ''),
                    'title': job_data.get('title', ''),
                    'link': job_data.get('permalink', ''),
                    'location': job_data.get('location', ''),
                    'date_found': datetime.now().strftime("%Y-%m-%d")
                }
            
            elif source == 'Indeed':
                job = {
                    'source': source,
                    'company': job_data.get('company', ''),
                    'title': job_data.get('jobtitle', ''),
                    'link': job_data.get('url', ''),
                    'location': job_data.get('location', ''),
                    'date_found': datetime.now().strftime("%Y-%m-%d")
                }
            
            elif source == 'Glassdoor':
                job = {
                    'source': source,
                    'company': job_data.get('employer', ''),
                    'title': job_data.get('jobTitle', ''),
                    'link': job_data.get('jobLink', ''),
                    'location': job_data.get('location', ''),
                    'date_found': datetime.now().strftime("%Y-%m-%d")
                }
            
            self.jobs.append(job)
            print(f"Found matching job: {job['title']} at {job['company']}")
            
        except Exception as e:
            print(f"Error processing job data: {str(e)}")

    def search_all(self):
        """Search all configured APIs"""
        self.search_linkedin()
        self.search_indeed()
        self.search_glassdoor()

    def export_to_excel(self, filename="job_listings.xlsx"):
        """Export results to Excel"""
        if not self.jobs:
            print("No jobs found to export")
            return
            
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"\nResults exported to {filename} with {len(self.jobs)} jobs") 