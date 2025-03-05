# Job Search Automation

A Python script that automates job searching across LinkedIn for project management and AI-related positions.

## Features

- Searches LinkedIn jobs for multiple keywords
- Configurable time range for job searches (default: 30 days)
- Scans job descriptions for visa/sponsorship requirements
- Saves results to Excel with:
  - Clickable application links
  - Multiple worksheets (one per search, timestamped)
  - Auto-adjusted column widths
- Tracks:
  - Company name
  - Job title
  - Location
  - Posting date
  - Visa/sponsorship information
  - Date found

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

Edit `src/config.py` to customize search keywords:

```python
KEYWORDS = [
    'project manager',
    'program manager',
    'product manager',
    'AI product manager',
    'AI program manager',
    'AI project manager',
    'AI product owner',
    'artificial intelligence product manager',
    'artificial intelligence program manager',
    'artificial intelligence project manager'
]
```

## Usage

Basic usage (searches last 30 days):
```bash
python src/main.py
```

Search with custom time range:
```bash
python src/main.py --days 7    # Search last 7 days
python src/main.py --days 14   # Search last 14 days
```

Get help:
```bash
python src/main.py --help
```

Results are saved to `job_listings.xlsx` with:
- New worksheet for each run, named with timestamp (e.g., `Jobs_202403041530`)
- Visa requirement information extracted from job descriptions
- Clickable links to job applications

## Project Structure
```
job-search/
├── src/
│   ├── main.py           # Script entry point
│   ├── job_searcher.py   # Job search implementation
│   └── config.py         # Search configuration
├── venv/                 # Virtual environment
└── README.md            # This file
```

## Notes
- Respects rate limiting with delays between requests
- Scans full job descriptions for visa/sponsorship requirements
- Provides context around visa-related terms found
- Exports results to Excel for easy filtering and tracking
