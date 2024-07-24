import requests
from bs4 import BeautifulSoup
import lxml


url = 'https://www.tarkov-goon-tracker.com/ru'
responce = requests.get(url).text
soup = BeautifulSoup(responce, 'lxml')

chek_goon_class = soup.find('div', 'sc-697118c5-1 hlSaaR')
result_goon = chek_goon_class.find_all('span')[0].text

result = f'В последний раз я замечал Гунов на локации: {result_goon}'

print(result)