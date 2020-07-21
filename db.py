import sqlite3
import datetime
import logging
# from tabulate import tabulate
from decos import log

conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы
@log
def create_table():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS jokes
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   joke varchar(500) NOT NULL, in_date TEXT NOT NULL)""")

@log
def add_joke(joke):
    date = datetime.datetime.today()
    # Вставляем данные в таблицу
    cursor.execute(f"INSERT INTO jokes (joke, in_date) \
                      VALUES ('{joke}', '{date.strftime('%d-%m-%Y')}')"
                   )
    conn.commit()

