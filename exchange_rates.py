import os
import re
import requests
from bs4 import BeautifulSoup as bs

"""
My first try to use web scraping with Python.
I'm currently interested in, where to buy dollars, or euro
with maximum profit.
"""

bm_url = "http://morskoybank.com"
rncb_url = "https://www.rncb.ru/fizicheskkim-litsam/valyutnye-operatsii/"
folder = 'exchange'
bm_req = requests.get(bm_url).text
rncb_req = requests.get(rncb_url).text
pattern = r"\d+,\d+"


try:
    os.mkdir(folder)
except OSError:
    print(f"Folder ({folder}) already exist")
finally:
    os.chdir(folder)


class GetBmExchangeRates():
    bm_currency_page = bs(bm_req, 'lxml')
    raw_currency_list = bm_currency_page.findChild('table', {'class': 'little'}).find_all('td')
    currency_list = re.findall(r"\d+,\d+", str(raw_currency_list))

    bm_exchange_rates = {
        'bm_dollar_purchase_rate' : float(currency_list[0].replace(',', '.')),
        'bm_dollar_selling_rate' : float(currency_list[1].replace(',', '.')),
        'bm_euro_purchase_rate' : float(currency_list[2].replace(',', '.')),
        'bm_euro_selling_rate' : float(currency_list[3].replace(',', '.'))
        }

    with open('mb_exchange.txt', 'w') as file:
        file.write(str(bm_exchange_rates))


class GetRncbExchangeRates():
    rncb_currency_page = bs(rncb_req, 'lxml')
    raw_currency_list = rncb_currency_page.findChild('table', {'class': 'cours'}).find_all('td')
    currency_list = re.findall(r"(\d{2}.\d{1,2})", str(raw_currency_list))

    rncb_exchange_rates = {
        'rncb_dollar_purchase_rate' : currency_list[0],
        'rncb_dollar_selling_rate' : currency_list[1],
        'rncb_euro_purchase_rate' : currency_list[2],
        'rncb_euro_selling_rate' : currency_list[3]
        }
    def display(self, info=rncb_exchange_rates):
        print(info)
    
    with open('rncb_exchange.txt', 'w') as file:
        file.write(str(rncb_exchange_rates))


def where_to_buy_currency():
    pass
     

def where_to_sell_currency():
    pass    

may_1 = GetRncbExchangeRates()
may_1.display()

    
    
