import requests
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bs4 import BeautifulSoup



def all_quest(per):
    text = []
    for i in per:
        text.append(i.text)
    return text


def prapor_quest_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for i in all_quest(name_quest_prapor):
        keyboard.add(KeyboardButton(text=i))
    return keyboard.adjust(2).as_markup()


url = 'https://tarkov.help/ru/'
responce = requests.get(url).text
soup = BeautifulSoup(responce, 'lxml')
traders = soup.find('div', id='quests').text


url_prapor = 'https://tarkov.help/ru/trader/prapor/quests'
responce_prapor = requests.get(url_prapor).text
soup_prapor = BeautifulSoup(responce_prapor, 'lxml')
name_quest_prapor = soup_prapor.find_all('a', 'article__title')


url_proba_pera = 'https://tarkov.help/ru/quest/proba_pera'
responce_proba_pera = requests.get(url_proba_pera).text
soup_proba_pera = BeautifulSoup(responce_proba_pera, 'lxml')
purpose_proba_pera = soup_proba_pera.find('div', 'quest-tab-grid').text
accomplishment_proba_pera = soup_proba_pera.find('section', 'quest-guide')
accomplishment_proba_pera_1 = accomplishment_proba_pera.find_all('div')
accomplishment_proba_pera_2 = (accomplishment_proba_pera_1[0].text + '\n' + accomplishment_proba_pera_1[2].text)
accomplishment_proba_pera_2 = accomplishment_proba_pera_2.replace("ЗаводУбийства", "Завод \nEбийства")


url_proverka_na_vshivost = 'https://tarkov.help/ru/quest/proverka-na-vshivost'
responce_proverka_na_vshivost = requests.get(url_proverka_na_vshivost).text
soup_proverka_na_vshivost = BeautifulSoup(responce_proverka_na_vshivost, 'lxml')
purpose_proverka_na_vshivost = soup_proverka_na_vshivost.find('div', 'quest-tab-grid').text
purpose_proverka_na_vshivost = purpose_proverka_na_vshivost.replace('\n', '')
purpose_proverka_na_vshivost = purpose_proverka_na_vshivost.replace(')Найти', ') \nНайти')
purpose_proverka_na_vshivost = purpose_proverka_na_vshivost.replace('часыПередать', "часы \nПередать")
accomplishment_proverka_na_vshivost = soup_proverka_na_vshivost.find('section', 'quest-guide')
accomplishment_proverka_na_vshivost_1 = accomplishment_proverka_na_vshivost.find_all('div')
accomplishment_proverka_na_vshivost_2 = accomplishment_proverka_na_vshivost_1[4].text
accomplishment_proverka_na_vshivost_3 = (accomplishment_proverka_na_vshivost_1[0].text + '\n' + accomplishment_proverka_na_vshivost_1[3].text + '\n'
                                         + '\n' + accomplishment_proverka_na_vshivost_2)
#print(accomplishment_proverka_na_vshivost_1[4].text)