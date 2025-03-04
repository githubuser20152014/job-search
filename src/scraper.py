from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

class JobScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Updated headless mode
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                     options=chrome_options)
        self.jobs = []

    def wait_and_find_elements(self, selector, timeout=10):
        """Wait for elements to be present and return them"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            print(f"Timeout waiting for elements with selector: {selector}")
            return []

    def search_company(self, company_name, company_url, keywords):
        try:
            print(f"Accessing {company_name} careers page...")
            self.driver.get(company_url)
            time.sleep(5)  # Initial wait for page load
            
            # Company-specific selectors and handling
            if company_name == 'Microsoft':
                # Microsoft's modern job listing selectors
                jobs = self.wait_and_find_elements("div[role='listitem']")
                for job in jobs:
                    try:
                        title = job.find_element(By.CSS_SELECTOR, "h3").text
                        if any(keyword.lower() in title.lower() for keyword in keywords):
                            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                            self.add_job(company_name, title, link)
                    except Exception as e:
                        print(f"Error processing Microsoft job: {str(e)}")

            elif company_name == 'Google':
                # Google's job listing selectors
                jobs = self.wait_and_find_elements("div.gc-card")
                for job in jobs:
                    try:
                        title = job.find_element(By.CSS_SELECTOR, ".gc-card__title").text
                        if any(keyword.lower() in title.lower() for keyword in keywords):
                            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                            self.add_job(company_name, title, link)
                    except Exception as e:
                        print(f"Error processing Google job: {str(e)}")

            elif company_name == 'Meta':
                # Meta's job listing selectors
                jobs = self.wait_and_find_elements("div._8sel")
                for job in jobs:
                    try:
                        title = job.find_element(By.CSS_SELECTOR, "._8see").text
                        if any(keyword.lower() in title.lower() for keyword in keywords):
                            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                            self.add_job(company_name, title, link)
                    except Exception as e:
                        print(f"Error processing Meta job: {str(e)}")

            elif company_name == 'IBM':
                # IBM's job listing selectors
                jobs = self.wait_and_find_elements("div.bx--card")
                for job in jobs:
                    try:
                        title = job.find_element(By.CSS_SELECTOR, ".bx--card__title").text
                        if any(keyword.lower() in title.lower() for keyword in keywords):
                            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                            self.add_job(company_name, title, link)
                    except Exception as e:
                        print(f"Error processing IBM job: {str(e)}")

        except Exception as e:
            print(f"Error scraping {company_name}: {str(e)}")

    def add_job(self, company, title, link):
        """Add a job to the jobs list"""
        job_data = {
            'company': company,
            'title': title,
            'link': link,
            'date_found': datetime.now().strftime("%Y-%m-%d")
        }
        self.jobs.append(job_data)
        print(f"Found matching job at {company}: {title}")

    def export_to_excel(self, filename="job_listings.xlsx"):
        if not self.jobs:
            print("No jobs found to export")
            return
            
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"\nResults exported to {filename} with {len(self.jobs)} jobs")

    def close(self):
        self.driver.quit() 