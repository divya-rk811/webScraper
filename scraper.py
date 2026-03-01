import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class NewsScraper:
    def __init__(self):
        # We are using a practice site, but you can use news blogs too
        self.url = "https://news.ycombinator.com/" 
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_headlines(self):
        print(f"--- Fetching latest tech news from {self.url} ---")
        try:
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Finding titles on Hacker News
            lines = soup.find_all('span', class_='titleline')
            
            news_list = []
            for line in lines[:10]:  # Get top 10
                title = line.text
                link = line.find('a')['href']
                news_list.append([title, link, datetime.now().strftime("%Y-%m-%d %H:%M")])
            
            return news_list
        except Exception as e:
            print(f"Error: {e}")
            return []

    def save_to_csv(self, data):
        filename = "trending_news.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Link', 'Scraped At'])
            writer.writerows(data)
        print(f"✅ Success! Data saved to {filename}")

if __name__ == "__main__":
    scraper = NewsScraper()
    data = scraper.fetch_headlines()
    if data:
        scraper.save_to_csv(data)
