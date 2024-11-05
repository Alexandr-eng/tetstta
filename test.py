import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    base_url = "https://quotes.toscrape.com"
    page_url = base_url
    quotes_data = []

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            quotes_data.append({
                'text': text,
                'author': author,
                'tags': tags
            })

        next_page = soup.find('li', class_='next')
        if next_page:
            page_url = base_url + next_page.find('a')['href']
        else:
            page_url = None

    with open('quotes.json', 'w') as json_file:
        json.dump(quotes_data, json_file, indent=4)

if __name__ == "__main__":
    scrape_quotes()