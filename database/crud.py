#crud.py
import asyncpg
from datetime import datetime
import logging
from config import Config

class Database:
    def __init__(self):
        self.conn = None

    async def connect(self):
        """Подключение к базе данных."""
        try:
            self.conn = await asyncpg.connect(Config.DATABASE_URL)
            logging.info("Успешное подключение к базе данных.")
            return True
        except Exception as e:
            logging.error(f"Ошибка при подключении к базе данных: {e}")
            return False

    async def close(self):
        """Закрытие соединения с базой данных."""
        if self.conn:
            await self.conn.close()
            logging.info("Соединение с базой данных закрыто.")


    async def register_user(self, user_id: int, username: str, first_name: str, last_name: str, age: int, workplace: str):
        """Регистрация пользователя, если он еще не зарегистрирован."""
        try:
            # Проверяем, существует ли пользователь
            user = await self.conn.fetchrow("""
                SELECT user_id FROM users WHERE user_id = $1
            """, user_id)
            
            if not user:
                # Если пользователь не существует, добавляем его
                await self.conn.execute("""
                    INSERT INTO users (user_id, username, first_name, last_name, age, workplace)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, user_id, username, first_name, last_name, age, workplace)
                logging.info(f"Пользователь {user_id} зарегистрирован.")
            else:
                logging.info(f"Пользователь {user_id} уже зарегистрирован.")
        except Exception as e:
            logging.error(f"Ошибка при регистрации пользователя: {e}")

    async def update_user_age(self, user_id: int, age: int):
        """Обновляет возраст пользователя."""
        try:
            await self.conn.execute("""
                UPDATE users SET age = $1 WHERE user_id = $2
                """, age, user_id)
            logging.info(f"Возраст пользователя {user_id} обновлен.")
        except Exception as e:
            logging.error(f"Ошибка при обновлении возраста: {e}")

    async def update_user_workplace(self, user_id: int, workplace: str):
        """Обновляет место работы/учебы пользователя."""
        try:
            await self.conn.execute("""
                UPDATE users SET workplace = $1 WHERE user_id = $2
            """, workplace, user_id)
            logging.info(f"Место работы/учебы пользователя {user_id} обновлено.")
        except Exception as e:
            logging.error(f"Ошибка при обновлении места работы/учебы: {e}")

    async def get_user_info(self, user_id: int):
        """Получает информацию о пользователе по его user_id."""
        try:
            user = await self.conn.fetchrow("""
                SELECT * FROM users WHERE user_id = $1
            """, user_id)
            return user
        except Exception as e:
            logging.error(f"Ошибка при получении информации о пользователе: {e}")
            return None

    async def add_event(self, user_id: int, event_name: str, event_description: str, event_date: datetime):
        """Добавление события в базу данных."""
        try:
            await self.conn.execute("""
                INSERT INTO events (user_id, event_name, event_description, event_date)
                VALUES ($1, $2, $3, $4)
            """, user_id, event_name, event_description, event_date)
            logging.info(f"Событие '{event_name}' добавлено в базу данных.")
        except Exception as e:
            logging.error(f"Ошибка при добавлении события: {e}")

    async def get_user_events(self, user_id: int):
        """Получение всех событий пользователя."""
        try:
            events = await self.conn.fetch("""
                SELECT * FROM events WHERE user_id = $1 ORDER BY event_date
            """, user_id)
            logging.info(f"Получено {len(events)} событий для пользователя {user_id}.")
            return events
        except Exception as e:
            logging.error(f"Ошибка при получении событий: {e}")
            return []
        
    async def update_user_age(self, user_id: int, age: int):
        """Обновляет возраст пользователя."""
        try:
            await self.conn.execute("""
                UPDATE users SET age = $1 WHERE user_id = $2
            """, age, user_id)
            logging.info(f"Возраст пользователя {user_id} обновлен.")
        except Exception as e:
            logging.error(f"Ошибка при обновлении возраста: {e}")

    async def update_user_workplace(self, user_id: int, workplace: str):
        """Обновляет место работы/учебы пользователя."""
        try:
            await self.conn.execute("""
                UPDATE users SET workplace = $1 WHERE user_id = $2
            """, workplace, user_id)
            logging.info(f"Место работы/учебы пользователя {user_id} обновлено.")
        except Exception as e:
            logging.error(f"Ошибка при обновлении места работы/учебы: {e}")
        

# Экспортируем функции для удобства
async def add_event(user_id: int, event_name: str, event_description: str, event_date: datetime):
    db = Database()
    await db.connect()
    await db.add_event(user_id, event_name, event_description, event_date)
    await db.close()

async def get_user_events(user_id: int):
    db = Database()
    await db.connect()
    events = await db.get_user_events(user_id)
    await db.close()
    return events