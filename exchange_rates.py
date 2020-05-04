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

        self.rates = {
            'dollars_purchase': float(currency_list[0].replace(',', '.')),
            'dollars_selling': float(currency_list[1].replace(',', '.'))
            }

    def __repr__(self):
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

        self.rates = {
            'dollars_purchase': float(currency_list[0]),
            'dollars_selling': float(currency_list[1]),
            }

    def save_rates(name=f'rncb_rates_{BmExchangeRates.exact_time()}.txt'):
        with open('name.txt', 'w') as file:
            file.write(str(rncb_rates))


class BuyingAndSelling():
    def __init__(self):
        bm = BmExchangeRates()
        rncb = RncbExchangeRates()
        self.buy_difference = abs(rncb.rates['dollars_selling'] - bm.rates['dollars_selling'])
        self.sell_difference = abs(rncb.rates['dollars_purchase'] - bm.rates['dollars_purchase'])
        if rncb.rates['dollars_selling'] <= bm.rates['dollars_selling']:
            print((
                "Now it’s better to buy dollars at the RNCB \n"
                f"Dollar rate in RNCB = {rncb.rates['dollars_selling']} \n"
                f"Dollar rate in BM = {bm.rates['dollars_selling']} \n"
                f"Difference between the dollar rates in this banks = {self.buy_difference}\n\n"))      
        else:
            print((
                "Now it’s better to buy dollars at the BM \n"
                f"Dollar rate in RNCB = {rncb.rates['dollars_selling']} \n"
                f"Dollar rate in BM = {bm.rates['dollars_selling']} \n"
                f"Difference between the dollar rates in this banks = {self.buy_difference}\n\n"))
            
        if rncb.rates['dollars_purchase'] >= bm.rates['dollars_purchase']:
            print((
                "Now it’s better to sell dollars at the RNCB \n"
                f"Dollar rate in RNCB = {rncb.rates['dollars_purchase']} \n"
                f"Dollar rate in BM = {bm.rates['dollars_purchase']} \n"
                f"Difference between the dollar rates in this banks = {self.sell_difference}"))     
        else:
            print((
                "Now it’s better to sell dollars at the BM \n"
                f"Dollar rate in RNCB = {rncb.rates['dollars_purchase']} \n"
                f"Dollar rate in BM = {bm.rates['dollars_purchase']} \n"
                f"Difference between the dollar rates in this banks = {self.sell_difference}"))
