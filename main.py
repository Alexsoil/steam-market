import requests
import urllib.request
import json
from bs4 import BeautifulSoup
import os


market_url = r'https://steamcommunity.com/market/listings/730/'

item_name = r'AWP | Sun in Leo (Field-Tested)'


url = market_url + item_name.replace(' ', r'%20')


html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, 'html.parser')

for imgtag in soup.find_all('img'):
    img_url = imgtag['src']
    if img_url[-9:] == '360fx360f':
        with open ('Images' + os.path.sep + item_name + '.png', 'wb') as handler:
            img_data = requests.get(img_url). content
            handler.write(img_data)


