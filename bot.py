import asyncio
import logging
import sys
import pathlib
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ContentType, Message, CallbackQuery, KeyboardButton, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
import random
import guuntraker
from Config_reader import config


# Config logging
logging.basicConfig(level=logging.INFO)

# BOt token and dispatcher
BOT = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# Class for FSM
class Linc(StatesGroup):
    linc = State()



# Function for registration in bot
@dp.message(Command('reg'))
async def reg (message: types.Message):
    script_path = pathlib.Path(sys.argv[0]).parent  # абсолютный путь до каталога, где лежит скрипт
    con = sqlite3.connect(script_path / "database.db")  # формируем абсолютный путь до файла базы
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))  # проверка на наличие id в бд
    user = cur.fetchone()
    if user is None:
        cur.execute(""" INSERT INTO users (user_id, user_name) VALUES (?, ?)""",
                    (message.from_user.id, message.from_user.full_name))
        con.commit()
        await message.answer(f'''Привет! Приятно познокомится {message.from_user.full_name}! \n
    Регистрирую вас в базе данных. \n
    Это необходимо для уведомлении вас о стримах.''')  # единоразовое приветствие
    else:  # если пользователь есть в бд
        otvet = ['И снова привет!', 'Опять работать?']
        await message.answer(random.choice(otvet))
    con.close()

# this function monitoring new users
@dp.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_member_handler(message: Message):
    new_member = message.new_chat_members[0]
    script_path = pathlib.Path(sys.argv[0]).parent  # абсолютный путь до каталога, где лежит скрипт
    con = sqlite3.connect(script_path / "database.db")  # формируем абсолютный путь до файла базы
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))# проверка на наличие id в бд
    user = cur.fetchone()
    # если id нет то добавляем
    if user is None:
        cur.execute(""" INSERT INTO users (user_id, user_name) VALUES (?, ?)""", (message.from_user.id, message.from_user.full_name))
        con.commit()
        await message.answer(f'''Привет! Приятно познокомится {message.from_user.full_name}! \n
Регистрирую вас в базе данных. \n
Это необходимо для уведомлении вас о стримах.''') # единоразовое приветствие
    else: # если пользователь есть в бд
        otvet = ['И снова привет!', 'Опять работать?']
        await message.answer(random.choice(otvet))
    con.close()

# Function for send start stream part one
@dp.message(Command('Stream'))
async def stream(message: types.Message, state: FSMContext):
    await state.set_state(Linc.linc)
    await message.answer('Введите ссылку на стрим')


# Function for send start stream part one
@dp.message(Linc.linc)
async def stream_one(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(linc=message.text)
    date = await state.get_data()
    script_path = pathlib.Path(sys.argv[0]).parent
    con = sqlite3.connect(script_path / "data_base_for_users_id")
    cur = con.cursor()
    users = cur.execute("""SELECT user_id FROM users""").fetchall()
    greeting_list = cur.execute('''SELECT text FROM greeting''').fetchone()
    con.commit()
    if message.chat.type == 'private':
        if message.from_user.id == 2123919405 or message.from_user.id == 814370409:
            for i in users:
                for user in i:
                    await bot.send_message(user, f'{date.get('linc')} \n{greeting_list[0]}')
    await state.clear()
    await message.answer('рассылка выполненна')


# Function for adding new greeting text
@dp.message(Command('text'))
async def text(message: types.Message, command: CommandObject):
    if message.from_user.id == 2123919405 or message.from_user.id == 814370409:
        script_path = pathlib.Path(sys.argv[0]).parent
        con = sqlite3.connect(script_path / "database.db")
        cur = con.cursor()
        message_text = command.args
        print(message_text, type(message_text))
        text = cur.execute('''SELECT text FROM greeting''').fetchone()
        if text is None:
            cur.execute('''INSERT INTO greeting(text) VALUES(?)''',
                        (message_text,))
            con.commit()
        else:
            cur.execute('''UPDATE greeting SET text = ? ''',
                    (message_text,))
            con.commit()
        print('\n\n\nТекст был успешно изменён! \n\n\n ')
    else:
        await message.answer('У вас нет прав на изменение текста приветствия')
        print('''\n\n\nНесанкционированная попытка изменения текста
           \nПопытка изменения текста была предотращена\n\n\n''')



# Function for check list all users registered in database from bot
@dp.message(Command('users'))
async def users (message: types.Message):
    try:
        script_path = pathlib.Path(sys.argv[0]).parent
        con = sqlite3.connect(script_path / "database.db")
        cur = con.cursor()
        users_db = cur.execute('''SELECT user_name FROM users''')
        text = ''
        for user_list in users_db:
            for user_string in user_list:
                text = f'{text + user_string}\n'
        await message.reply(f'Все пользователи зарегистрированные в базе данных \n{text}')
        con.close()
        print('\n\n\nФункция успешно выполнена\nВсе пользователи зарегистрированные в базе данных выведены\n\n\n')
    except:
        print('\n\n\nОШИБКА\nВывод зарегистрированных пользователей не осуществлён из за ошибки\n\n\n')
        con.close()


@dp.message(F.text)
async def quest(message: types.Message):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    request = message.text[0].upper() + message.text[1:].lower()
    cur.execute("SELECT purponse, guide FROM quest WHERE name_quest = ?", (request,))
    quest_info = cur.fetchone()
    await message.reply(f"{request.upper()}\n\nЦель: {quest_info[0]}\n\nГайд: {quest_info[1]}")
        
    
        
        

async def main():
    await dp.start_polling(BOT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())