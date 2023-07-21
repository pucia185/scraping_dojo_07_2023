import os
import json
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class QuotesScraper:
    load_dotenv()
    def __init__(self):
        self.input_url = os.getenv('INPUT_URL')
        self.input_host = os.getenv('INPUT_HOST')
        self.output_file = os.getenv('OUTPUT_FILE')
        self.driver = None
        self.wait = None

    @staticmethod
    def scrape_page(url):
        return json.loads(
            BeautifulSoup(requests.get(url).text, 'lxml').find_all('script')[1].text.split('for (var i in data)')[0].split(
                'var data =')[-1].strip().rstrip(';'))

    def scrape_quotes(self):
        url = self.input_url
        all_quotes = []
        while True:
            all_quotes.extend(self.scrape_page(url))
            next_page = BeautifulSoup(requests.get(url).text, 'lxml').find('li', {'class': 'next'})
            if not next_page:
                break
            else:
                url = self.input_host + next_page.find('a').get('href')
        return all_quotes

    def write_quotes_to_file(self, quotes):
        with open(self.output_file, mode='w') as f:
            json.dump(quotes, f)

    def run(self):
        quotes = self.scrape_quotes()
        self.write_quotes_to_file(quotes)
        print(f"Scraped {len(quotes)} quotes from all pages to output.jsonl.")