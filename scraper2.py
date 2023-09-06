import os
import requests
from bs4 import BeautifulSoup as soup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class PinterestExtractor:

    def __init__(self):
        self.post_links = []

    def extract_links_from_local_html(self, html_path):
        """Extract links from local HTML."""
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        html = soup(html_content, 'html.parser')
        link_elements = html.find_all("a", target="_self")
        return [link['href'] for link in link_elements if link.has_attr('href')]

    def get_url_from_pinterest_post(self, post_link):
        """Get the desired URL from within the Pinterest post."""
        if not post_link.startswith("http"):
            return None
        res = requests.get(post_link)

    def extract_all(self, html_path):
        self.post_links = self.extract_links_from_local_html(html_path)
        extracted_urls = []
        with ThreadPoolExecutor() as executor:
            extracted_urls = list(executor.map(self.get_url_from_pinterest_post, self.post_links))
        return extracted_urls

    def save_to_excel(self, urls, filename="output.xlsx"):
        df = pd.DataFrame({"Links": urls})
        df.to_excel(filename, index=False)
        print(f"Saved extracted links to {filename}")


if __name__ == "__main__":
    local_html_path = "pinterest.html"  # Update with your path
    extractor = PinterestExtractor()
    urls = extractor.extract_all(local_html_path)
    extractor.save_to_excel(urls)
