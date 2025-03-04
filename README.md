# Job Search Automation

A Python script that automates job searching across LinkedIn for project management and AI-related positions.

## Features

- Searches LinkedIn jobs for multiple keywords
- Filters for jobs posted in the last 30 days
- Saves results to Excel with:
  - Clickable application links
  - Multiple worksheets (one per search, timestamped)
  - Auto-adjusted column widths
- Tracks:
  - Company name
  - Job title
  - Location
  - Posting date
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

Run the script:
```bash
python src/main.py
```

Results are saved to `job_listings.xlsx` with a new worksheet created for each run, named with timestamp (e.g., `Jobs_202403041530`).

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
- Exports results to Excel for easy filtering and tracking
