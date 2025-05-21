import requests
from logic.website_fetcher import WebsiteFetcher


fetcher = WebsiteFetcher("https://bbc.com")
try:
    html = fetcher.fetch()
    print(html[:500])  # Print first 500 characters
except requests.RequestException as e:
    print("Failed to fetch:", e)