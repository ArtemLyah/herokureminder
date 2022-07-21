import sqlite3
from datetime import datetime


connection = sqlite3.connect("reminder.db")
cursor = connection.cursor()

def add_user(user_id):
    cursor.execute(f"SELECT * FROM user_settings WHERE user_id={user_id}")
    if not cursor.fetchall():
        cursor.execute(f"INSERT INTO user_settings(user_id) VALUES({user_id})")
        connection.commit()

def get_from_user_settings(user_id, args:list):
    cursor.execute(f"SELECT {','.join(args)} FROM user_settings WHERE user_id={user_id}")
    res = cursor.fetchall()[0][0]
    return res
def set_user_settings(user_id, kwargs:dict):
    s = ""
    for item in kwargs.items():
        s += item[0]+"="+repr(item[1])
    cursor.execute(f"UPDATE user_settings SET {s} WHERE user_id={user_id}")
    connection.commit()

def create_task(user_id, text, date=None):
    if date:
        if len(date.split()) == 1:
            utc = float(get_from_user_settings(user_id, ["utc"]))
            date += datetime.strftime(datetime.fromtimestamp(datetime.now().timestamp()+utc*3600), " %d/%m/%Y")
        date = datetime.strptime(date, "%H:%M:%S %d/%m/%Y").timestamp()
        sql = f"INSERT INTO tasks(user_id, text, date) VALUES({user_id}, '{text.strip()}', {date})"
    else:
        sql = f"INSERT INTO tasks(user_id, text) VALUES({user_id}, '{text.strip()}')"
    cursor.execute(sql)
    connection.commit()

def get_task(user_id, text=""):
    if text:
        sql = f"SELECT id, text, date FROM tasks WHERE user_id={user_id} AND text='{text.strip()}' ORDER BY date"
    else:
        sql = f"SELECT id, text, date FROM tasks WHERE user_id={user_id} ORDER BY date"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
def remove_task(user_id, task_id):
    sql = f"DELETE FROM tasks WHERE id={task_id} AND user_id={user_id}"
    cursor.execute(sql)
    connection.commit()
    

def get_alarm_tasks():
    # utc = float(get_from_user_settings(user_id, ["utc"]))
    europe_time = datetime.now()
    print(europe_time(europe_time.astimezone()))
    sql = f"SELECT user_id, text FROM tasks WHERE date <= {europe_time}"
    cursor.execute(sql)
    return cursor.fetchall()
def remove_date_from_task(user_id, text):
    sql = f"UPDATE tasks SET date=NULL WHERE user_id={user_id} AND text='{text.strip()}'"
    cursor.execute(sql)
    connection.commit()