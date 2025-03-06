from openai import OpenAI
import logging
from config import Config

class OpenAIClient:
    def __init__(self):
        # Инициализируем клиент OpenAI
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def get_advice(self, prompt: str):
        try:
            # Используем новый API для создания завершения
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Используем модель GPT-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,  # Ограничиваем количество токенов
            )
            # Возвращаем текст ответа
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Ошибка при запросе к OpenAI: {e}")
            return "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."