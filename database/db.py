import random
import sqlite3
import datetime

from log.decos import log

conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы
@log
def create_table():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS jokes
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   joke varchar(500) NOT NULL, in_date TEXT NOT NULL)""")

@log
def create_table_bday():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS bday
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   name varchar(500) NOT NULL, b_date TEXT NOT NULL)""")


def get_bdate():
    arr = []
    days_to = 365
    near_date = datetime.date.today()
    today = datetime.date.today()
    for row in cursor.execute('select * from bday'):
        arr.append(row[2])
    for born in arr:
        born_s = born.split('-')
        birthday = datetime.date(today.year, int(born_s[1]), int(born_s[2]))
        if birthday > today:
            delta = birthday - today
            delta = str(delta)
            new = delta.split()[0]
            if int(new) < int(days_to):
                days_to = new
                near_date = born
    # b_day = '-'.join(near_date)
    # print(b_day)
    cursor.execute(f'select name from bday where b_date="{near_date}"')
    result = cursor.fetchone()
    result = str(result).replace("('", "", 1)
    result = str(result).replace("',)", "")
    # [имя фамилия, дней до др, дата рождения]
    res = [result, days_to, near_date]
    return res

get_bdate()

@log
def add_joke(joke):
    date = datetime.datetime.today()
    # Вставляем данные в таблицу
    cursor.execute(f"INSERT INTO jokes (joke, in_date) \
                      VALUES ('{joke}', '{date.strftime('%d-%m-%Y')}')"
                   )
    conn.commit()


@log
def get_joke():
    joke_arr = []
    for row in cursor.execute('select * from jokes'):
        joke_arr.append(row[0])
    random_joke = random.choice(joke_arr)
    statement = f"select joke from jokes where id={random_joke}"
    cursor.execute(statement)
    result = cursor.fetchone()
    result = str(result).replace("('", "", 1)
    result = str(result).replace("',)", "")
    result = str(result).replace("\n", " ")
    return result
