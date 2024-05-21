import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import subprocess


class Scraper:


    def __init__(self,initial_url) -> None:
        self.initial_url = initial_url
        self.self.visited_urls = set()        

    def is_internal_link(self,url):
        # Parse the URL and check if it's from cro.ie
        parsed_url = urlparse(url)
        return parsed_url.netloc == "cro.ie"

    def is_valid_link(self,url):
        # Check if the URL contains "gazette" or is a direct link to a PDF file
        return "gazette" in url.lower() or url.endswith(".pdf")

    def download_file(self,url, dest_folder):
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


    def crawl_and_download(self,url, folder_path):
        # Add the current URL to the set of visited URLs
        self.visited_urls.add(url)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    absolute_url = urljoin(url, href)

                    # Check if the link is an internal cro.ie link and meets the criteria
                    if self.is_internal_link(absolute_url) and self.is_valid_link(absolute_url) and absolute_url not in self.visited_urls:
                        print(f"Visiting URL: {absolute_url}")
                        self.crawl_and_download(absolute_url, folder_path)
                        if '.pdf' in absolute_url:                        
                            print(f"Downloading PDF: {absolute_url}")
                            self.download_file(absolute_url, folder_path)

        except requests.RequestException as e:
            print(f"Error accessing URL: {url} - {e}")


