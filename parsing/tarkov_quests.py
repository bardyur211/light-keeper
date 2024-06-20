import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://tarkov.help/ru/'
responce = requests.get(url).text
soup = BeautifulSoup(responce, 'lxml')
traders = soup.find('div', id='quests').text

url_prapor = 'https://tarkov.help/ru/trader/prapor/quests'
responce_prapor = requests.get(url_prapor).text
soup_prapor = BeautifulSoup(responce_prapor, 'lxml')
all_quests_prapor = soup_prapor.find('div', 'articles-wrapper')
cards_quest_prapor = all_quests_prapor.find('div', 'articles')
name_quest_prapor = cards_quest_prapor.find_all('a')



print(name_quest_prapor)