import requests_cache
# Initialize requests cache to avoid hitting the server too frequently
requests_cache.install_cache('serebii_cache', expire_after=3600)  # Cache for 1 hour
import requests
from bs4 import BeautifulSoup

def get_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # Serebii blocks some default clients
    page = None
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        if response.from_cache:
            print(f"Using cached page for {url}")
        page = response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    if page:
        return BeautifulSoup(page, "html.parser")
    return None

