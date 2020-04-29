import os
import re
import requests
from bs4 import BeautifulSoup as bs

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


def get_bm_exchange_rates():
    bm_currency_page = bs(bm_req, 'lxml')
    raw_currency_list = bm_currency_page.findChild('table', {'class': 'little'}).find_all('td')
    currency_list = re.findall(r"\d+,\d+", str(raw_currency_list))
    bm_exchange_rates = {
        'bm_dollar_purchase_rate' : currency_list[0],
        'bm_dollar_selling_rate' : currency_list[1],
        'bm_euro_purchase_rate' : currency_list[2],
        'bm_euro_selling_rate' : currency_list[3]
        }

    with open('exchange.txt', 'w') as file:
        file.write(bm_exchange_rates)
