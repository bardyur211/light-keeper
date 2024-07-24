from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from bs4 import BeautifulSoup
from tqdm import tqdm
from database import *
import requests
import pathlib
import sys


URL_TARKOV_VIKI_QUEST = 'https://escapefromtarkov.fandom.com/ru/wiki/Квесты'
URL = URL_TARKOV_VIKI_QUEST
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}

soup = BeautifulSoup(requests.get(URL, headers=HEADERS).text, 'lxml')
guide_quest = []
name_quest = {}
quest_prapor = {}
name_trader = ['Prapor', 'Therapist', 'Fence', 'Skier', 'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']


def set_table_quest():
    for trader in tqdm(name_trader, desc='Processing traders', position=0, leave=True):
        table = soup.find('table', {'class': f'{trader}-content'})
        table = table.find_all('tbody')
        for i in table:
            table = i.find_all('tr')
            for i in table:
                table = i.find_all('th')
                for i in table:
                    table = i.find_all('a')
                    for name_quest_1 in table:
                        name_quest[name_quest_1.text] = f'https://escapefromtarkov.fandom.com{name_quest_1['href']}'

def info_quest():
    purponce = []
    linc = name_quest.values()
    linc_1 = list(linc)[1:]
    for i in tqdm(linc_1, desc='Processing quest info', position=0, leave=True):
        try:
            r = requests.get(i, headers=HEADERS)
            soup = BeautifulSoup(r.text, 'lxml')
            purpose = soup.find('span', id='Цель(и)')
            head_2 = purpose.findParent()
            result = head_2.find_next_sibling().text
            purponce.append(result)
        except:
            purponce.append('Нет информация о цели квеста')
    return purponce

def guide():
    text = ''
    lst = []
    linc = name_quest.values()
    linc_1 = list(linc)[1:]
    current_linc = None
    for i in tqdm(linc_1, desc='Processing quest guide', position=0, leave=True):
        try:
            r = requests.get(i, headers=HEADERS)
            soup = BeautifulSoup(r.text, 'lxml')
            guide = soup.find('span', id='.D0.92.D1.8B.D0.BF.D0.BE.D0.BB.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5')
            head_2 = guide.findParent()
            result = head_2.find_all_next('p')
            for i in result:
                text += f'{i.text}'
            if current_linc != i:
               guide_quest.append(text)
               text = ''
               current_linc = i
            guide_quest.append(text)
        except:
            guide_quest.append('Нет информации о гайде квеста')

def data_rasyr(name: dict, data: list):
    result = {}
    # name.pop('')
    for key, value in zip(name.keys(), data):
            result[key] = value
    return result

def set_db():
    script_path = pathlib.Path(sys.argv[0]).parent
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    purponce_1 = info_quest()
    name_quest.pop('')
    my_list = [item for item in guide_quest if item != '']
    guide = data_rasyr(name_quest, guide_quest)
    for name, purponce, guide_1 in tqdm(zip(name_quest, purponce_1, my_list), desc='Updating quest info', position=0, leave=True):
        cur.execute('''INSERT INTO quest (name_quest, purponse, guide) VALUES (?, ?, ?)''', (name, purponce, guide_1,))
        con.commit()
    con.close()
    
    
def quest_keyboard():
    name_quest_for_keyboard = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    name_quest_in_db = cur.execute('''SELECT name_quest FROM quest''').fetchall()
    print(name_quest_in_db)    


def main():
    set_table_quest()
    info_quest()
    guide()
    set_db()

if __name__ == '__main__':
    main()
