from database import *
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

x = input('...')
y = cur.execute('''SELECT purponse, guide FROM quest WHERE name_quest = ?''', (x,)).fetchall()

for i in y:
    print(i[0]) 
