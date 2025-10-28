import requests
import json
from bs4 import BeautifulSoup
from os import write

req = requests.get(r'https://steamcommunity.com/market/listings/730/G3SG1%20%7C%20Green%20Apple%20(Factory%20New)')

data = req.text

soup = BeautifulSoup(data, 'html.parser')

headers = soup.find_all('div', class_='market-listing market_recent_listing_row')

print()

