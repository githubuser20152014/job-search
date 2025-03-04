# Job Search Automation

A Python script that automates job searching across major tech companies by searching LinkedIn job listings for specified roles.

## Setup

1. Create and activate virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
```

2. Install required packages:

```bash
pip install requests pandas beautifulsoup4 feedparser openpyxl
```

## Configuration

Edit `src/config.py` to customize:

```python
# Companies to search
COMPANIES = [
    'Microsoft',
    'Google',
    'Meta',
    'IBM'
]

# Job titles to search for
KEYWORDS = [
    'project manager',
    'program manager',
    'product manager'
]
```

## Usage

Run the script:
```bash
python src/main.py
```

The script will:
1. Search LinkedIn jobs for each company and keyword combination
2. Save results to `job_listings.xlsx` with:
   - Company name
   - Job title
   - Location
   - Application link
   - Date found

## Project Structure
```
job-search/
├── src/
│   ├── main.py           # Main script
│   ├── job_searcher.py   # Job search implementation
│   └── config.py         # Search configuration
├── venv/                 # Virtual environment
└── README.md            # This file
```

## Notes
- Respects rate limiting with delays between requests
- Exports results to Excel for easy filtering and tracking
