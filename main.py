import requests
from urllib import parse
from time import sleep
from forex_python.converter import CurrencyRates
import pandas as pd

def price_to_float(price: str):
    price = price.replace(',', '.')
    price = price.replace('-', '0')
    return float(price[:-1])


market_url = r'https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name='

c = CurrencyRates()
rate = c.get_rate('USD', 'EUR')
del c
print(f'Current rate of exchange from USD to EUR is {rate}.')


with open('items.txt', 'r') as itemfile:
    data_list = []
    for line in itemfile.readlines():
        item_name = line.strip()
        item_url = parse.quote(item_name)
        item_data = requests.get(market_url + item_url).json()
        if item_data is None:
            print(f'Reached max requests, waiting 60 seconds and retrying.')
            sleep(60)
            item_data = requests.get(market_url + item_url).json()
        item_data['name'] = item_name
        data_list.append(item_data)
    daily_data = pd.DataFrame(data_list)
    daily_data.drop(columns=["success"], inplace=True)
    daily_data = daily_data.loc[:, ['name', 'lowest_price', 'volume', 'median_price']]
    print(daily_data)

        # item_price = item_data.get('lowest_price')
        # if item_price is not None:
        #     float_price = price_to_float(item_price)
        # else:
        #     print(f'Something went wrong with item {item_name}. Skipping.')
        #     continue

        # print(f'{item_name}: {float_price:.2f}€')



# item_name = 'AWP | Sun in Leo (Field-Tested)'
# print(parse.quote(item_name))
# data = requests.get(market_url + parse.quote(item_name)).json()
# print(data)





# url = market_url + item_name.replace(' ', r'%20')


# html = urllib.request.urlopen(url)

# soup = BeautifulSoup(html, 'html.parser')

# for imgtag in soup.find_all('img'):
#     img_url = imgtag['src']
#     if img_url[-9:] == '360fx360f':
#         with open ('Images' + os.path.sep + item_name + '.png', 'wb') as handler:
#             img_data = requests.get(img_url). content
#             handler.write(img_data)

# for price in soup.find_all('span', class_='market_listing_price_with_fee'):
#     print(float(price.contents[0].strip()[1:6]))




