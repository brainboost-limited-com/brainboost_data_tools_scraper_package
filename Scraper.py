import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import subprocess


# Set the initial URL to start crawling
base_url = "https://cro.ie/cro-gazette-publications/"

# Set up a set to keep track of visited URLs to avoid revisiting
visited_urls = set()

def is_internal_link(url):
    # Parse the URL and check if it's from cro.ie
    parsed_url = urlparse(url)
    return parsed_url.netloc == "cro.ie"

def is_valid_link(url):
    # Check if the URL contains "gazette" or is a direct link to a PDF file
    return "gazette" in url.lower() or url.endswith(".pdf")

def download_file(url, dest_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    
    # Extract filename from the URL
    file_name = url.split('/')[-1]
    
    # Set the full path of the destination file
    dest_file_path = os.path.join(dest_folder, file_name)
    
    # Use subprocess to execute wget command
    try:
        subprocess.run(['wget', url, '-P', dest_folder])
        print(f"File downloaded successfully to: {dest_file_path}")
    except Exception as e:
        print(f"Failed to download file from {url}: {e}")


def crawl_and_download(url, folder_path):
    # Add the current URL to the set of visited URLs
    visited_urls.add(url)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                absolute_url = urljoin(url, href)

                # Check if the link is an internal cro.ie link and meets the criteria
                if is_internal_link(absolute_url) and is_valid_link(absolute_url) and absolute_url not in visited_urls:
                    print(f"Visiting URL: {absolute_url}")
                    crawl_and_download(absolute_url, folder_path)
                    if '.pdf' in absolute_url:                        
                        print(f"Downloading PDF: {absolute_url}")
                        download_file(absolute_url, folder_path)

    except requests.RequestException as e:
        print(f"Error accessing URL: {url} - {e}")

# Create a folder path for saving PDF files
pdf_folder = "/brainboost/brainboost_financial/financial_cro/gazettes"

# Start crawling from the base URL and download PDF files
crawl_and_download(base_url, pdf_folder)
