import psycopg2
from datetime import datetime
from configs.env_reader import env_config
import asyncio
from psycopg2 import OperationalError
import logging



class BotDB:

    def __init__(self):
        self.connection = None
        self.conn = None
        self.cursor = None

    async def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=env_config.DB_HOST,  # Use upper case as per the config
                dbname=env_config.DB_NAME,
                user=env_config.DB_USER,
                password=env_config.DB_USER_PASS.get_secret_value(),
                port=env_config.DB_PORT
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database.")
        except OperationalError as e:
            print(f"Error: Unable to connect to the database: {e}")

    # Пример функции в db.py
    async def check_free_room(self, game, sum):
        try:
            self.cursor.execute("""
                SELECT room_id 
                FROM rooms 
                WHERE game = %s AND "sum" <= %s AND is_free = TRUE 
                LIMIT 1
            """, (game, sum))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            logging.error(f"Error in check_free_room: {e}")
            return None

    async def create_room_game(self, game, sum):
        try:
            self.cursor.execute("""
                INSERT INTO rooms (game, sum, is_free) 
                VALUES (%s, %s, TRUE)
            """, (game, sum))
            self.connection.commit()  # Подтверждение изменений в базе данных
        except Exception as e:
            logging.error(f"Error in create_room_game: {e}")
            self.connection.rollback()  # Откат транзакции в случае ошибки

    async def get_lines_not_done_topup(self):
        self.cursor.execute("SELECT COUNT (*) FROM payments WHERE (accrued = true and done = false)")
        return self.cursor.fetchone()[0]

    async def get_user_exists(self, user_id, arg='user_id ='):
        self.cursor.execute(f"SELECT id FROM users WHERE {arg} %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    async def get_user_id(self, user_id):
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_user_name(self, user_id):
        self.cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_user_lastname(self, user_id):
        self.cursor.execute("SELECT lastname FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_user_username(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_user_date(self, user_id):
        self.cursor.execute("SELECT join_date FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_rules_accept(self, user_id):
        self.cursor.execute("SELECT rules_acc FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_ban(self, user_id):
        self.cursor.execute("SELECT ban FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def set_rules_accept(self, user_id):
        self.cursor.execute("UPDATE users SET rules_acc = True WHERE user_id = %s", (user_id,))
        return self.conn.commit()

    async def add_user(self, user_id, name, lastname, username):
        self.cursor.execute(
            "INSERT INTO users (user_id, name, lastname, username, balance) VALUES (%s, %s, %s, %s, 10000)",
            (user_id, name, lastname, username))
        return self.conn.commit()

    async def set_user_block_bot(self, user_id, arg):
        self.cursor.execute("UPDATE users SET bot_blocked = %s WHERE user_id = %s", (arg, user_id,))
        return self.conn.commit()

    async def get_bot_block(self, user_id):
        self.cursor.execute("SELECT bot_blocked FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_user_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_topup_accured(self, top_id):
        self.cursor.execute("SELECT accrued FROM payments WHERE int_pay = %s", (top_id,))
        return self.cursor.fetchone()[0]

    async def get_topup_done(self, top_id):
        self.cursor.execute("SELECT done FROM payments WHERE int_pay = %s", (top_id,))
        return self.cursor.fetchone()[0]

    async def set_topup_done(self, top_id):
        self.cursor.execute("UPDATE payments SET done = True, time_done = %s WHERE int_pay = %s",
                            (str(datetime.now()), top_id,))
        return self.conn.commit()

    async def get_topup_sum(self, top_id):
        self.cursor.execute("SELECT sum FROM payments WHERE int_pay = %s", (top_id,))
        return self.cursor.fetchone()[0]

    async def set_topup_balance(self, user_id, sum_topup):
        self.cursor.execute("UPDATE users SET balance = balance+ %s WHERE user_id = %s", (sum_topup, user_id,))
        return self.conn.commit()

    async def set_withdraw_balance(self, user_id, sum):
        self.cursor.execute("UPDATE users SET balance = balance- %s WHERE user_id = %s", (sum, user_id,))
        return self.conn.commit()

    async def update_data(self, name, lastname, username, user_id):
        self.cursor.execute("UPDATE users SET name = %s, lastname = %s, username = %s  WHERE user_id = %s",
                            (name, lastname, username, user_id,))
        return self.conn.commit()

    # More methods as per your original code...

    async def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
