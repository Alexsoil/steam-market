import requests
from urllib import parse
from time import sleep
from datetime import datetime
from forex_python.converter import CurrencyRates
import pandas as pd
from os import makedirs

def price_to_float(price: str) -> float: 
    price = price.replace(',', '.')
    price = price.replace('-', '0')
    return float(price[:-1])

def percentage_difference(new_price: float, old_price: float) -> str:
    return str(round((new_price / old_price - 1) * 100, 2)) + '%'

def colour(text: str, colour: str):
    if colour == 'red':
        return '\033[31m' + text + '\033[0m'
    elif colour == 'green':
        return '\033[32m' + text + '\033[0m'
    elif colour == 'yellow':
        return '\033[33m' + text + '\033[0m'
    elif colour == 'magenta':
        return '\033[35m' + text + '\033[0m'
    elif colour == 'cyan':
        return '\033[36m' + text + '\033[0m'
    else:
        return '\033[37m' + text + '\033[0m'

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
        # print(item_name)
        while item_data is None:
            print(f'Reached max requests, waiting 60 seconds and retrying.')
            sleep(65)
            item_data = requests.get(market_url + item_url).json()
        item_data['name'] = item_name
        if item_data.get('lowest_price') is not None:
            item_data['lowest_price'] = price_to_float(item_data['lowest_price'])
        else:
            item_data['lowest_price'] = 0
        if item_data.get('median_price') is not None:
            item_data['median_price'] = price_to_float(item_data['median_price'])
        else:
            item_data['median_price'] = 0
        if item_data.get('volume') is not None:
            item_data['volume'] = int(item_data['volume'].replace(',', ''))
        else:
            item_data['volume'] = 0
        data_list.append(item_data)
    daily_data = pd.DataFrame(data_list)
    daily_data.drop(columns=["success"], inplace=True)
    daily_data = daily_data.loc[:, ['name', 'lowest_price', 'median_price', 'volume']]
    
    makedirs('data/', exist_ok=True)
    try:
        latest_data = pd.read_csv('data/latest.csv')
        complete_data = daily_data.merge(latest_data[['name', 'lowest_price']], left_on='name', right_on='name', suffixes=('_new', '_old'))
        complete_data['percentage_diff'] = complete_data['lowest_price_new'] / complete_data['lowest_price_old']
        complete_data['percentage_diff'] = round((complete_data['percentage_diff'] - 1), 2)
        complete_data = complete_data.loc[:, ['name', 'lowest_price_new', 'lowest_price_old', 'percentage_diff', 'median_price', 'volume']]
        # print(complete_data)
        daily_data.to_csv('data/latest.csv')
        # daily_data.to_csv(datetime.now())

        print(f'{'Item Name':^55} | {'New Price':^10} | {'Old Price':^10} | {'Difference':^12} | {'Volume':^8}')
        for idx, row in complete_data.iterrows():
            price = row['lowest_price_new']
            if price >= 5 and price < 10.0:
                price = colour(f'{price:4.2f}', 'magenta')
            elif price >= 10.0 and price < 25.0:
                price = colour(f'{price:4.2f}', 'cyan')
            elif price >= 25.0:
                price = colour(f'{price:4.2f}', 'yellow')
            else:
                price = colour(f'{price:4.2f}', '')
            percent = row['percentage_diff']
            if percent > 0:
                percent = colour(f'{percent:.2%}', 'green')
            elif percent < 0:
                percent = colour(f'{percent:.2%}', 'red')
            else:
                percent = colour(f'{percent:.2%}', '')
            price_old = f'{row['lowest_price_old']:.2f}'
            print(f'{row['name']:<55} | {price:^19} | {price_old:^10} | {percent:^21} | {row['volume']:<10}')
        print(colour('PINGU', 'yellow'))
            
    except FileNotFoundError:
        print(f'No historical data found, presenting daily data.')
        print(daily_data)
        daily_data.to_csv('data/latest.csv')
