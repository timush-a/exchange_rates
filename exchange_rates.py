import os
import re
import time
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


try:
    os.mkdir(folder)
except OSError:
    print(f"Folder ({folder}) already exist")
finally:
    os.chdir(folder)


def exact_time():
        return time.strftime('%Y-%m-%d__%H-%m-%S', time.localtime())


class BmExchangeRates():
    bm_currency_page = bs(bm_req, 'lxml')
    raw_currency_list = bm_currency_page.findChild('table', {'class': 'little'}).find_all('td')
    currency_list = re.findall(r"\d+,\d+", str(raw_currency_list))

    bm_rates = {
        'dollars_purchase': float(currency_list[0].replace(',', '.')),
        'dollars_selling': float(currency_list[1].replace(',', '.'))
        }

    with open(f'bm_rates_{exact_time()}.txt', 'w') as file:
        file.write(str(bm_rates))


class RncbExchangeRates():
    rncb_currency_page = bs(rncb_req, 'lxml')
    raw_currency_list = rncb_currency_page.findChild('table', {'class': 'cours'}).find_all('td')
    currency_list = re.findall(r"(\d{2}.\d{1,2})", str(raw_currency_list))  # this pattern will be used to find numbers of the form like 99.99

    rncb_rates = {
        'dollars_purchase': float(currency_list[0]),
        'dollars_selling': float(currency_list[1]),
        }

    def display(self, info=rncb_rates):
        print(info)

    with open(f'rncb_rates_{exact_time()}.txt', 'w') as file:
        file.write(str(rncb_rates))


def where_to_sell_dollars():

    bm_rates = BmExchangeRates().bm_rates
    rncb_rates = RncbExchangeRates().rncb_rates

    if rncb_rates['dollars_purchase'] >= bm_rates['dollars_purchase']:
        difference = rncb_rates['dollars_purchase'] - bm_rates['dollars_purchase']
        print('You should to sell dollars in RNCB')
        print(f'Difference of rates is equal {difference}')
    else:
        difference = bm_rates['dollars_purchase'] - rncb_rates['dollars_purchase']
        print('You should to sell dollars in Sea Bank')
        print(f'Difference of rates is equal {difference}')


def where_to_buy_dollars():

    bm_rates = BmExchangeRates().bm_rates
    rncb_rates = RncbExchangeRates().rncb_rates
    if rncb_rates['dollars_selling'] >= bm_rates['dollars_selling']:
        difference = rncb_rates['dollars_selling'] - bm_rates['dollars_selling']
        print('You should to buy dollars in RNCB')
        print(f'Difference of rates is equal {difference}')
    else:
        difference = bm_rates['dollars_selling'] - rncb_rates['dollars_selling']
        print('You should to buy dollars in Sea Bank')
        print(f'Difference of rates is equal {difference}')
