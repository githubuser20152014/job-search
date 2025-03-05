from job_searcher import JobSearcher
from config import KEYWORDS
import argparse
import time

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Search for jobs on LinkedIn')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days to look back (default: 30)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize searcher with days parameter
    searcher = JobSearcher(days_back=args.days)
    
    print(f"Starting job search (looking back {args.days} days)...")
    searcher.search_linkedin_jobs()
    
    # Export results
    searcher.export_to_excel()

if __name__ == "__main__":
    main() 