import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Kolya252003",
    host="127.0.0.1",
    port="5432"
)

cur = con.cursor()


def check_and_add_user(message, name='Nick', age='NULL', sex='NULL', state='Старт'):
    if cur.execute(f'SELECT name FROM user_questionnaire WHERE id = {message.from_user.id}') is None:
        cur.execute(
            f"INSERT INTO user_questionnaire (id,name,age,sex,state) VALUES ({message.from_user.id}, '{name}', {age}, '{sex}', '{state}')"
        )
        con.commit()


def get_current_state(user_id):
    cur.execute(f'SELECT state FROM user_questionnaire WHERE id = {user_id}')
    state = cur.fetchone()
    return state[0]


def set_new_state(user_id, state_value):
    cur.execute(f"UPDATE user_questionnaire SET state = '{state_value}' WHERE id = {user_id}")
    con.commit()
