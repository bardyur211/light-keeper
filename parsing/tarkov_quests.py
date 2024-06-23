import requests
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bs4 import BeautifulSoup


img_number = 0


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

url_piknik_so_strelboj = 'https://tarkov.help/ru/quest/piknik-so-strelboj'
responce_piknik_so_strelboj = requests.get(url_piknik_so_strelboj).text
soup_piknik_so_strelboj = BeautifulSoup(responce_piknik_so_strelboj, 'lxml')
purpose_piknik_so_strelboj = soup_piknik_so_strelboj.find('div', 'quest-tab-goal').text
purpose_piknik_so_strelboj = purpose_piknik_so_strelboj.strip('\n')
accomplishment_piknik_so_strelboj = soup_piknik_so_strelboj.find('section', 'quest-guide').text
accomplishment_piknik_so_strelboj =accomplishment_piknik_so_strelboj.replace('Как выполнить квест?', '')
accomplishment_piknik_so_strelboj = accomplishment_piknik_so_strelboj.strip('\n')
accomplishment_piknik_so_strelboj =accomplishment_piknik_so_strelboj.replace('Найти диких на карте', '')



url_posylka_iz_proshlogo = 'https://tarkov.help/ru/quest/posylka-iz-proshlogo'
responce_posylka_iz_proshlogo = requests.get(url_posylka_iz_proshlogo).text
soup_posylka_iz_proshlogo = BeautifulSoup(responce_posylka_iz_proshlogo, 'lxml')
purpose_posylka_iz_proshlogo = soup_posylka_iz_proshlogo.find('div', 'quest-tab-grid').text
purpose_posylka_iz_proshlogo = purpose_posylka_iz_proshlogo.strip('\n').splitlines()
def delete_none(list):
    for i in list:
        if i == '':
             (list[i])
    return(i)
print(delete_none(purpose_posylka_iz_proshlogo))
print(purpose_posylka_iz_proshlogo)