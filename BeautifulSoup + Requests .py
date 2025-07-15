from bs4 import BeautifulSoup

import requests

url = 'https://www.scrapethissite.com/pages/forms/'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

print(soup)