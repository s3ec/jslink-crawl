import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to extract JavaScript links from a single page
def get_js_links_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', src=True)
        return [urljoin(url, tag['src']) for tag in script_tags]
    except requests.exceptions.RequestException:
        return []

# Function to find all internal links on a page
def get_internal_links(url, base_domain):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for tag in soup.find_all('a', href=True):
            link = urljoin(url, tag['href'])
            # Add only internal links
            if urlparse(link).netloc == base_domain:
                links.add(link)
        return links
    except requests.exceptions.RequestException:
        return set()

# Function to crawl the domain and extract JavaScript links
def crawl_domain(start_url, max_pages=100):
    visited = set()
    to_visit = set([start_url])
    base_domain = urlparse(start_url).netloc
    all_js_links = set()

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        print(f"Crawling: {current_url}")
        js_links = get_js_links_from_page(current_url)
        all_js_links.update(js_links)

        internal_links = get_internal_links(current_url, base_domain)
        to_visit.update(internal_links - visited)

    return all_js_links

# Main program: Ask user for the domain (without the URL scheme)
if __name__ == "__main__":
    domain = input("Enter the domain (e.g., example.com): ").strip()

    # Prepend 'https://' to the domain if the user did not include it
    if not domain.startswith("http"):
        start_url = f"https://{domain}"
    else:
        start_url = domain

    print(f"\nCrawling the domain: {start_url}")
    all_js_links = crawl_domain(start_url)
    
    print("\nAll JavaScript Links:")
    for link in all_js_links:
        print(link)
