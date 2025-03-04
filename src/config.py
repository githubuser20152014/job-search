# API Configuration
APIS = {
    'LinkedIn': {
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET',
        'base_url': 'https://api.linkedin.com/v2/jobs-search'
    },
    'Indeed': {
        'publisher_id': 'YOUR_PUBLISHER_ID',
        'base_url': 'https://api.indeed.com/ads/apisearch'
    },
    'Glassdoor': {
        'partner_id': 'YOUR_PARTNER_ID',
        'key': 'YOUR_API_KEY',
        'base_url': 'https://api.glassdoor.com/api/api.htm'
    }
}

# Companies to search for
COMPANIES = [
    'Microsoft',
    'Google',
    'Meta',
    'IBM'
]

# Keywords to search for
KEYWORDS = [
    'project manager',
    'program manager',
    'product manager'
]

# Delay between requests (in seconds)
DELAY = 2 