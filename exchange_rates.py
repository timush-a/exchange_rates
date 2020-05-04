import os
import re
import time
import requests
from bs4 import BeautifulSoup as bs

"""
My first try to use web scraping with Python.
I'm currently interested in where to buy dollars or euro
with maximum profit.
"""


class BmExchangeRates():
    bm_url = "http://morskoybank.com"

    def __init__(self, url=bm_url):
        request = requests.get(url).text

        currencies_page = bs(request, 'lxml')
        raw_currency_list = currencies_page.findChild('table', {'class': 'little'}).find_all('td')
        currency_list = re.findall(r"(\d{2}.\d{1,2})", str(raw_currency_list))  # this pattern will be used to find numbers of the form like 99.99

        rates = {
            'dollars_purchase': float(currency_list[0].replace(',', '.')),
            'dollars_selling': float(currency_list[1].replace(',', '.'))
            }

    def __str__(self, rates):
        return rates

    def exact_time():
        return time.strftime('%Y-%m-%d__%H-%m-%S', time.localtime())

    def save_rates(self, name=f'bm_rates_{exact_time()}.txt'):
        with open('name.txt', 'w') as file:
            file.write(str(bm_rates))


class RncbExchangeRates(BmExchangeRates):
    rncb_url = "https://www.rncb.ru/fizicheskkim-litsam/valyutnye-operatsii/"

    def __init__(self, url=rncb_url):
        request = requests.get(url).text

        currencies_page = bs(request, 'lxml')
        raw_currency_list = currencies_page.findChild('table', {'class': 'cours'}).find_all('td')
        currency_list = re.findall(r"(\d{2}.\d{1,2})", str(raw_currency_list))

        rates = {
            'dollars_purchase': float(currency_list[0]),
            'dollars_selling': float(currency_list[1]),
            }

    def display(self):
        print(rates)

    def save_rates(name=f'rncb_rates_{BmExchangeRates.exact_time()}.txt'):
        with open('name.txt', 'w') as file:
            file.write(str(rncb_rates))


class BuyingAndSelling():

    bm = BmExchangeRates()
    rncb = RncbExchangeRates()

    def where_to_sell_dollars(self):
        if rncb.rates['dollars_purchase'] >= bm.rates['dollars_purchase']:
            difference = rncb.rates['dollars_purchase'] - bm.rates['dollars_purchase']
            print('You should to sell dollars in RNCB')
            print(f'Difference of rates is equal {difference}')
        else:
            difference = bm.rates['dollars_purchase'] - rncb.rates['dollars_purchase']
            print('You should to sell dollars in Sea Bank')
            print(f'Difference of rates is equal {difference}')

    def where_to_buy_dollars(self):
        if rncb.rates['dollars_selling'] >= bm.rates['dollars_selling']:
            difference = rncb.rates['dollars_selling'] - bm.rates['dollars_selling']
            print(
                f"""You should to buy dollars in RNCB /n
                Dollar rate in a RNCB ---- {rncb.rates['dollars_selling']} /n
                Dollar rate in a BM ---- {bm.rates['dollars_selling']} /n
                Difference between the dollar rates in this banks is equal {difference}"""
                )
        
        else:
            difference = bm.rates['dollars_selling'] - rncb.rates['dollars_selling']
            print(
                f"""You should to buy dollars in RNCB /n
                Dollar rate in a RNCB ---- {rncb.rates['dollars_selling']} /n
                Dollar rate in a BM ---- {bm.rates['dollars_selling']} /n
                Difference between the dollar rates in this banks is equal {difference}"""
                )
        
