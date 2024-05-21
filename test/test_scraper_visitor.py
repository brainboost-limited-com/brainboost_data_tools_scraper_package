import test.Scraper as Scraper


my_scraper = Scraper()

# Create a folder path for saving PDF files
pdf_folder = "/brainboost/brainboost_financial/financial_cro/gazettes"

# Start crawling from the base URL and download PDF files
crawl_and_download(self.initial_url, pdf_folder)