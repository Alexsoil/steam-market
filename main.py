import requests
import urllib.request
import json
from bs4 import BeautifulSoup
from os import write

url = r'https://steamcommunity.com/market/listings/730/G3SG1%20%7C%20Green%20Apple%20(Factory%20New)'

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, 'html.parser')

image_link = soup.find('img', {"class": "market_listing_item_img_container"})

print(image_link)

# for div in soup.find('div', {"class": "market_listing_item_name_block"}):
#     print(div.get_text())
