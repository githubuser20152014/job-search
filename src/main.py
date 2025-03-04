from job_searcher import JobSearcher
from config import KEYWORDS
import time

def main():
    searcher = JobSearcher()
    
    print("Starting job search...")
    searcher.search_linkedin_jobs()
    
    # Export results
    searcher.export_to_excel()

if __name__ == "__main__":
    main() 