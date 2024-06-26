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

import parsing.tarkov_quests
from Config_reader import config
from parsing import guuntraker, tarkov_quests, dict

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
    con = sqlite3.connect(script_path / "data_base_for_users_id")  # формируем абсолютный путь до файла базы
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


# Function for send registration in bot
@dp.message(Command("x")) # rename function
async def x (message: types.Message):
    while True:
        await message.answer("""Дорогие друзья! Хочу напомнить вам о необходимости регистрации в базе данных, \n так как в противном случае бот не сможет вам присылать уведомления
о начале стрима. \n \n Зарегистрироваться можно, написав команду /reg, после чего бот автоматически занесёт вас в базу данных.""")
        await asyncio.sleep(86400)


# Check ID new user-admin
@dp.message(Command('admin_id'))
async def admin(message: types.Message):
    print(message.from_user.id)


# this function monitoring new users
@dp.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_member_handler(message: Message):
    new_member = message.new_chat_members[0]
    script_path = pathlib.Path(sys.argv[0]).parent  # абсолютный путь до каталога, где лежит скрипт
    con = sqlite3.connect(script_path / "data_base_for_users_id")  # формируем абсолютный путь до файла базы
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
        con = sqlite3.connect(script_path / "data_base_for_users_id")
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
        con = sqlite3.connect(script_path / "data_base_for_users_id")
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


@dp.message(Command('service'))
async def quest(message: types.Message):
    keyboard_traders = ReplyKeyboardBuilder()
    keyboard_traders.row(
        types.KeyboardButton(text='Местонахождения Гунов')
    )
    keyboard_traders.row(
        types.KeyboardButton(text='Прапор'),
        types.KeyboardButton(text='Терапевт'),
        types.KeyboardButton(text='Скупщик')
    )
    keyboard_traders.row(
        types.KeyboardButton(text='Лыжник'),
        types.KeyboardButton(text='Миротворец'),
        types.KeyboardButton(text='Механик')
    )
    keyboard_traders.row(
        types.KeyboardButton(text='Барахольщик'),
        types.KeyboardButton(text='Егерь'),
        types.KeyboardButton(text='Смотритель Маяка')
    )
    keyboard_traders.row(
        types.KeyboardButton(text='Назад')
    )
    await message.answer('Выберите услугу',
                         reply_markup=keyboard_traders.as_markup(resize_keyboard=True, one_time_keyboard=True))


@dp.message(F.text.lower() == 'местонахождения гунов')
async def goon(message: types.Message):
    await message.reply(guuntraker.result)


@dp.message(F.text.lower() == 'прапор')
async def prapor(message: types.Message):
    await message.answer('Выберите квест', reply_markup=tarkov_quests.prapor_quest_keyboard())



@dp.message(F.text.lower()=='терапевт')
async def terapevt(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='скупщик')
async def trader(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='лыжник')
async def snowraner(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='миротворец')
async def mirotvorec(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='механик')
async def mechanic(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='барахольщик')
async def trader_avito(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='егерь')
async def forest_man(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов

@dp.message(F.text.lower()=='смотритель маяка')
async def lighthouse_keeper(message: types.Message):
    await message.answer('Проверка пройденна')# сдесь должен быть список всех квестов


@dp.message(F.text)
async def quest(message: types.Message):
    if message.text in dict.prapor:
        await message.answer(dict.prapor[message.text])

async def main():
    await dp.start_polling(BOT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())