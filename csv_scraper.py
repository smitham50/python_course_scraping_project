import requests
from csv import DictWriter
from bs4 import BeautifulSoup
from random import choice
from time import sleep

base_url = 'http://quotes.toscrape.com'

def scrape_quotes():
    url = '/page/1'
    entries = []

    while url:
        response = requests.get(f'{base_url}{url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.select('.quote')

        for quote in quotes:
            entries.append({
                "text": quote.select('.text')[0].get_text(),
                "author": quote.select('.author')[0].get_text(),
                "bio_url": quote.find('a')['href']
            })

        next_btn = soup.find(class_='next')
        url = next_btn.find('a')['href'] if next_btn else None
        sleep(2)

    return entries

entries = scrape_quotes()

with open ('quotes.csv', 'w') as csvfile:
    headers = ['text', 'author', 'bio_url']
    csv_writer = DictWriter(csvfile, fieldnames=headers)
    csv_writer.writeheader()

    for row in entries:
        csv_writer.writerow(row)


