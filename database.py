import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL
)""")


cur.execute('''CREATE TABLE IF NOT EXISTS greeting(
            text STRING 
            linc STRING 
)''')



cur.execute('''CREATE TABLE IF NOT EXISTS quest(
    name_quest STRING,
    purponse STRING,
    guide STRING)''')



con.commit()