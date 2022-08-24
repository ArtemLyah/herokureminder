import psycopg2
connection = psycopg2.connect(
    host = "ec2-54-75-26-218.eu-west-1.compute.amazonaws.com",
    database = "d311bpqh4vdsbb",
    user="jygzulixavhtch",
    password="d53a8835396e5e76256f0f5dfb7a0d2d67d68f3992c6566844c94d864470faa1"
)
cursor = connection.cursor()
# manage users
def add_user(user_id):
    cursor.execute(f"SELECT * FROM user_settings WHERE user_id='{user_id}'")
    if not cursor.fetchall():
        cursor.execute(f"INSERT INTO user_settings(user_id) VALUES('{user_id}')")
        connection.commit()
def get_from_user_settings(user_id, args:list):
    cursor.execute(f"SELECT {','.join(args)} FROM user_settings WHERE user_id='{user_id}'")
    res = cursor.fetchall()[0][0]
    return res
def set_user_settings(user_id, **kwargs):
    s = ""
    for item in kwargs.items():
        s += item[0]+"="+repr(item[1])
    cursor.execute(f"UPDATE user_settings SET {s} WHERE user_id='{user_id}'")
    connection.commit()

# manage tasks
def create_task(user_id, text):
    sql = f"INSERT INTO tasks(user_id, text) VALUES('{user_id}', '{text.strip()}')"
    cursor.execute(sql)
    connection.commit()
def get_task(user_id, text=""):
    if text:
        sql = f"SELECT id, text FROM tasks WHERE user_id='{user_id}' AND text='{text.strip()}' ORDER BY id"
    else:
        sql = f"SELECT id, text FROM tasks WHERE user_id='{user_id}' ORDER BY id"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
def remove_task(user_id, task_id):
    sql = f"DELETE FROM tasks WHERE id={task_id} AND user_id='{user_id}'"
    cursor.execute(sql)
    connection.commit()