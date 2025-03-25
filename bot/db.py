import asyncpg
from datetime import datetime
from configs.env_reader import env_config
import asyncio
import logging

class BotDB:

    def __init__(self):
        self.conn = None  # Используем self.conn для подключения

    async def connect(self):
        try:
            self.conn = await asyncpg.create_pool(
                host=env_config.DB_HOST,
                database=env_config.DB_NAME,
                user=env_config.DB_USER,
                password=env_config.DB_USER_PASS.get_secret_value(),
                port=env_config.DB_PORT
            )
            print("Connected to the database.")
        except Exception as e:
            print(f"Error: Unable to connect to the database: {e}")
            logging.error(f"Error: Unable to connect to the database: {e}")

    async def check_free_room(self, game, sum):
        try:
            async with self.conn.acquire() as connection:
                result = await connection.fetch("""
                    SELECT room_id 
                    FROM rooms 
                    WHERE game = $1 AND "sum" <= $2 AND is_free = TRUE 
                    LIMIT 1
                """, game, sum)
                if result:
                    return result[0]['room_id']  # Извлекаем room_id из результата
                else:
                    return None
        except Exception as e:
            logging.error(f"Error in check_free_room: {e}")
            return None

    async def create_room_game(self, game, sum):
        try:
            async with self.conn.acquire() as connection:
                await connection.execute("""
                    INSERT INTO rooms (game, sum, is_free) 
                    VALUES ($1, $2, TRUE)
                """, game, sum)
        except Exception as e:
            logging.error(f"Error in create_room_game: {e}")

    async def get_lines_not_done_topup(self):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT COUNT(*) FROM payments WHERE (accrued = TRUE AND done = FALSE)")
            return result

    async def get_user_exists(self, user_id, arg='user_id ='):
        async with self.conn.acquire() as connection:
            result = await connection.fetch("SELECT id FROM users WHERE " + arg + " $1", user_id)
            return bool(len(result))

    async def get_user_id(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT id FROM users WHERE user_id = $1", user_id)
            return result

    async def get_user_name(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT name FROM users WHERE user_id = $1", user_id)
            return result

    async def get_user_lastname(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT lastname FROM users WHERE user_id = $1", user_id)
            return result

    async def get_user_username(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT username FROM users WHERE user_id = $1", user_id)
            return result

    async def get_user_date(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT join_date FROM users WHERE user_id = $1", user_id)
            return result

    async def get_rules_accept(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT rules_acc FROM users WHERE user_id = $1", user_id)
            return result

    async def get_ban(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT ban FROM users WHERE user_id = $1", user_id)
            return result

    async def set_rules_accept(self, user_id):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE users SET rules_acc = TRUE WHERE user_id = $1", user_id)

    async def add_user(self, user_id, name, lastname, username):
        async with self.conn.acquire() as connection:
            await connection.execute(
                "INSERT INTO users (user_id, name, lastname, username, balance) VALUES ($1, $2, $3, $4, 10000)",
                user_id, name, lastname, username)

    async def set_user_block_bot(self, user_id, arg):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE users SET bot_blocked = $1 WHERE user_id = $2", arg, user_id)

    async def get_bot_block(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT bot_blocked FROM users WHERE user_id = $1", user_id)
            return result

    async def get_user_balance(self, user_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT balance FROM users WHERE user_id = $1", user_id)
            return result

    async def get_topup_accured(self, top_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT accrued FROM payments WHERE int_pay = $1", top_id)
            return result

    async def get_topup_done(self, top_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT done FROM payments WHERE int_pay = $1", top_id)
            return result

    async def set_topup_done(self, top_id):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE payments SET done = TRUE, time_done = $1 WHERE int_pay = $2",
                                    str(datetime.now()), top_id)

    async def get_topup_sum(self, top_id):
        async with self.conn.acquire() as connection:
            result = await connection.fetchval("SELECT sum FROM payments WHERE int_pay = $1", top_id)
            return result

    async def set_topup_balance(self, user_id, sum_topup):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE users SET balance = balance + $1 WHERE user_id = $2", sum_topup, user_id)

    async def set_withdraw_balance(self, user_id, sum):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE users SET balance = balance - $1 WHERE user_id = $2", sum, user_id)

    async def update_data(self, name, lastname, username, user_id):
        async with self.conn.acquire() as connection:
            await connection.execute("UPDATE users SET name = $1, lastname = $2, username = $3 WHERE user_id = $4",
                                    name, lastname, username, user_id)

    async def add_user_to_game_room(self, room_id, user_id, user_balance, game, sum):
        try:
            async with self.conn.acquire() as connection:
                # Проверяем, есть ли уже пользователь в этой комнате
                existing_user = await connection.fetchval("""
                    SELECT 1 FROM game_room_users WHERE room_id = $1 AND user_id = $2
                """, room_id, user_id)
                if existing_user:
                    print(f"User {user_id} is already in room {room_id}.")
                    return  # Пользователь уже в комнате, не добавляем снова

                # Если нет, добавляем пользователя
                await connection.execute("""
                    INSERT INTO game_room_users (room_id, user_id, user_balance, game, bet_sum) 
                    VALUES ($1, $2, $3, $4, $5)
                """, room_id, user_id, user_balance, game, sum)
                print(f"User {user_id} added to game room {room_id} successfully.")
        except Exception as e:
            logging.error(f"Error in add_user_to_game_room: {e}")

    async def add_user_to_game_room(self, room_id, user_id, user_balance, game, sum, game_id):
        try:
            await self.conn.execute("""
                INSERT INTO game_room_users (room_id, user_id, user_balance, game, bet_sum, game_id) 
                VALUES ($1, $2, $3, $4, $5, $6)
            """, room_id, user_id, user_balance, game, sum, game_id)
            print(f"User {user_id} added to game room {room_id} successfully.")
        except Exception as e:
            logging.error(f"Error in add_user_to_game_room: {e}")

    async def get_no_warned_player_lines(self):
        try:
            async with self.conn.acquire() as connection:
                result = await connection.fetchval("SELECT COUNT(*) FROM player_lines WHERE warned = FALSE")
                return result if result else 0
        except Exception as e:
            logging.error(f"Error in get_no_warned_player_lines: {e}")
            return 0  # Возвращаем 0 в случае ошибки, чтобы избежать NoneType

    async def set_room_full(self, room_id):
        try:
            async with self.conn.acquire() as connection:
                await connection.execute("""
                    UPDATE game_rooms
                    SET is_full = TRUE
                    WHERE room_id = $1
                """, room_id)
                print(f"Room {room_id} set to full.")
        except Exception as e:
            logging.error(f"Error in set_room_full: {e}")

    async def win_num_check(self, room_id):
        try:
            async with self.conn.acquire() as connection:
                result = await connection.fetchval("""
                    SELECT COUNT(*) 
                    FROM game_room_users 
                    WHERE room_id = $1 AND is_winner = TRUE
                """, room_id)
                return result if result else 0
        except Exception as e:
            logging.error(f"Error in win_num_check: {e}")
            return 0

    async def update_win_num_in(self, win_num, room_id):
        async with self.conn.acquire() as connection:
            query = """
            UPDATE games SET win_num = $1 WHERE room_id = $2
            """
            await connection.execute(query, win_num, room_id)

    async def add_user_to_game_room(self, room_id, user_id, user_balance, game, sum):
        try:
            async with self.conn.acquire() as connection:
                await connection.execute("""
                    INSERT INTO game_room_users (room_id, user_id, user_balance, game, bet_sum) 
                    VALUES ($1, $2, $3, $4, $5)
                """, room_id, user_id, user_balance, game, sum)
                print(f"User {user_id} added to game room {room_id} successfully.")
        except Exception as e:
            logging.error(f"Error in add_user_to_game_room: {e}")

    async def close(self):
        if self.conn:
            await self.conn.close()
            print("Database connection closed.")
