from bs4 import BeautifulSoup
import requests 


url = 'https://www.scrapethissite.com/pages/forms/'


page = requests.get(url)

soup = BeautifulSoup(page.text, 'html') 

print(soup)

soup.find('div')

soup.find_all('div')


soup.find_all('p')


soup.find('p' , class_ = 'lead').text


soup.find('p' , class_ = 'lead').text.strip()


soup.find('th').text.strip()