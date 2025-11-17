import requests

class CS2handler:
    market_link = r'https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name='

    def __init__(self):
        bleh = 'AWP | Sun in Leo (Field-Tested)'
        response = requests.get(self.market_link + bleh)
        res_dict = response.json()

    def _get_market_data(self, item_name: str):
        response = requests.get(self.market_link + item_name)
        data_dict = response.json()
        if data_dict[0].value and len(data_dict) > 1:
            return data_dict
        else:
            return None
        
    def _get_item_image(self, item_name: str):
        pass
        
            
        

Pingas = CS2handler()
