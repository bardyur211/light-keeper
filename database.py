import sqlite3

con = sqlite3.connect('data_base_for_users_id')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL
)""")


cur.execute('''CREATE TABLE IF NOT EXISTS greeting(
            text STRING 
            linc STRING 
)''')



con.commit()