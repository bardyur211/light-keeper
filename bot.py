import asyncio
import logging
import sys
from database import *
import pathlib
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import ContentType, Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
import random
from Config_reader import config
from aiogram.client.session.aiohttp import AiohttpSession
from Function import function


logging.basicConfig(level=logging.INFO)


BOT = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


class Linc(StatesGroup):
    linc = State()


@dp.message(Command('reg'))
async def reg(message: types.Message):



# Функция для напоминания регистрации в боте
@dp.message(Command("x"))
async def x (message: types.Message):
    while True:
        await message.answer("""Дорогие друзья! Хочу напомнить вам о необходимости регистрации в базе данных, \n так как в противном случае бот не сможет вам присылать уведомления
о начале стрима. \n \n Зарегистрироваться можно, написав команду /reg, после чего бот автоматически занесёт вас в базу данных.""")
        await asyncio.sleep(86400)


@dp.message(Command('admin_id'))
async def admin(message: types.Message):
    print(message.from_user.id)


# Эта функция нужна для приветствия пользователем который вступил в чат
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


@dp.message(Command('Stream'))
async def stream(message: types.Message, state: FSMContext):
    await state.set_state(Linc.linc)
    await message.answer('Введите ссылку на стрим')


@dp.message(Linc.linc)
async def stream_one(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(linc = message.text) # доделать комманду добавлением рассылки
    date = await state.get_data()
    print(date, type(date))
    lst = []
    script_path = pathlib.Path(sys.argv[0]).parent
    con = sqlite3.connect(script_path / "data_base_for_users_id")
    cur = con.cursor()
    users = cur.execute("""SELECT user_id FROM users""").fetchall()
    greeting_list = cur.execute('''SELECT text FROM greeting''').fetchone()
    #linc_bd_one = cur.execute('''INSERT INTO greeting(linc) VALUES(?)''', ())
    con.commit()
    if message.chat.type == 'private':
        if message.from_user.id == 2123919405 or message.from_user.id == 814370409:
            for greeting in greeting_list:
                for i in users:
                    for user in i:
                            await bot.send_message(user, f'{date.get('linc')} \n\n {greeting}')
        await message.answer('рассылка выполненна')

            

#@dp.message(Command("Stream"))
#async def mailing (message: types.message, command: CommandObject, bot: Bot):
#    link_list = command.args.split(" ", maxsplit=1)
#    column = -1
#    script_path = pathlib.Path(sys.argv[0]).parent
#    con = sqlite3.connect(script_path / "data_base_for_users_id")
#    cur = con.cursor()
#    if message.chat.type == 'private':
#        if message.from_user.id == 2123919405 or message.from_user.id == 814370409:
#            text = f'''Привет, друг! Заходи на стрим, я всегда тебе рад! \n {link}'''
#            users = cur.execute("""SELECT user_id FROM users""").fetchall()
#            for i in users:
#                for user in i:
#                    mes = comd_text(text_list,link(link_list))
#                    await bot.send_message(user, mes)
#            await message.answer('рассылка выполненна')
#        else:
#            await message.answer("К сожалению этой коммандой может пользоваться только админ!")



@dp.message(Command('text'))
async def text(message: types.Message, command: CommandObject):
    try:
        if message.from_user.id == 2123919405 or message.from_user.id == 814370409:
            script_path = pathlib.Path(sys.argv[0]).parent
            con = sqlite3.connect(script_path / "data_base_for_users_id")
            cur = con.cursor()
            message_text = command.args
            print(message_text, type(message_text))
            text = cur.execute('''SELECT text FROM greeting''')
            con.commit()
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
    except:
        print('''\n\n\n       Внимание!!!
        \nОшибка при выполнении функции\n\n\n''')


@dp.message(Command('users'))
async def users (message: types.Message):
    try:
        script_path = pathlib.Path(sys.argv[0]).parent
        con = sqlite3.connect(script_path / "data_base_for_users_id")
        cur = con.cursor()
        users_db = cur.execute('''SELECT user_name FROM users''')
        for user_list in users_db:
            for user_string in user_list:
                message_answer_user = f'{user_string}\n'
                await message.reply(f'Все пользователи зарегистрированные в базе данных \n{message_answer_user}')
        print('\n\n\nФункция успешно выполнена\nВсе пользователи зарегистрированные в базе данных выведены\n\n\n')
    except:
        print('\n\n\nОШИБКА\nВывод зарегистрированных пользователей не осуществлён из за ошибки\n\n\n')
     


async def main():
    await dp.start_polling(BOT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())