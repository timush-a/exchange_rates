import os
import requests
from bs4 import BeautifulSoup as bs
from lxml import html

url = "http://morskoybank.com"
folder = 'exchange'
req = requests.get(url).text


try:
    os.mkdir(folder)
except OSError:
    print(f"Folder ({folder}) already exist")
finally:
    os.chdir(folder)


##with open('exchange.txt', 'w') as file:
##    file.write(req.text)
soup = bs(req, 'lxml')

currency_list = soup.find_all('table', {'class': 'little'})
print(currency_list)

##tree = html.fromstring(req)
##print(tree)
##print(tree.xpath('//table[@class="little"]')[0])
