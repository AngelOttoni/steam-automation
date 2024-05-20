import requests
from bs4 import BeautifulSoup
import csv
import re
import os
from datetime import datetime

# Constants
OUTPUT_DIR = 'data/raw'
OUTPUT_FILE = 'steam_data.csv'
MAX_LINES = 100

# Function to get the total number of pages
def get_total_pages(url):
    response = requests.get(url)
    response.raise_for_status()
    doc = BeautifulSoup(response.content, 'html.parser')
    pagination = doc.find('div', {'class': 'search_pagination_right'})
    if pagination:
        total_pages = int(pagination.find_all('a')[-2].text)
    else:
        total_pages = 1
    return total_pages

# Function to extract information from games
def extract_game_info(game):
    name = game.find('span', {'class': 'title'}).text
    published_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip()

    original_price_elem = game.find('div', {'class': 'discount_original_price'})
    discount_price_elem = game.find('div', {'class': 'discount_final_price'})

    if original_price_elem:
        original_price = original_price_elem.text.strip()
    elif discount_price_elem:
        original_price = discount_price_elem.text.strip()
    else:
        original_price = 'NaN'

    if discount_price_elem:
        discount_price = discount_price_elem.text.strip()
    else:
        discount_price = 'NaN'

    if original_price == 'Free' or discount_price == 'Free':
        original_price = discount_price = 'Free'
    elif original_price != 'NaN' and discount_price == 'NaN':
        discount_price = original_price

    review_summary = game.find('span', {'class': 'search_review_summary'})
    reviews_html = review_summary['data-tooltip-html'] if review_summary else 'NaN'

    match = re.search(r'(\d+,*\d*)\s+user reviews', reviews_html)
    reviews_number = match.group(1).replace(',', '') if match else 'NaN'

    return name, published_date, original_price, discount_price, reviews_number

# Function to scrape the page
def scrape_page(url, search_filter, writer):
    total_pages = get_total_pages(url)
    line_count = 0

    for page in range(1, total_pages + 1):
        response = requests.get(f"{url}&page={page}")
        response.raise_for_status()
        doc = BeautifulSoup(response.content, 'html.parser')
        games = doc.find_all('div', {'class': 'responsive_search_name_combined'})

        for game in games:
            game_info = extract_game_info(game)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([*game_info, search_filter, timestamp])
            line_count += 1
            if line_count >= MAX_LINES:
                print(f"Reached {MAX_LINES} lines for filter '{search_filter}'.")
                return
        print(f"Completed page {page}/{total_pages} for filter '{search_filter}'.")

# Main function to perform scraping
def main(search_filters):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'release_date', 'initial_price', 'discount_price', 'reviews', 'search_filter', 'timestamp'])

        for search_filter in search_filters:
            print(f"Starting scraping for filter '{search_filter}'.")
            url = f'https://store.steampowered.com/search/?filter={search_filter}'
            scrape_page(url, search_filter, writer)
            print(f"Completed scraping for filter '{search_filter}'.")

    print(f"Scraping completed. Data saved to '{output_path}'.")

# Search filters for scraping
SEARCH_FILTERS = ['topsellers', 'mostplayed', 'newreleases', 'upcoming']

# Execute the main function
if __name__ == "__main__":
    main(SEARCH_FILTERS)