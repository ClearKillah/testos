import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.filters import Command
from aiohttp import web
import logging
import ssl

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv('8039344227:AAEDCP_902a3r52JIdM9REqUyPx-p2IVtxA')
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN не установлен в переменных окружения")

# URL вашего веб-приложения на Railway
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://testos-production.up.railway.app')

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(
                text="Открыть чат",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы открыть анонимный чат.",
        reply_markup=keyboard
    )

# Обработчик для получения данных из веб-приложения
@dp.message(lambda message: message.web_app_data is not None)
async def web_app_handler(message: types.Message):
    logging.info(f"Получены данные из веб-приложения: {message.web_app_data.data}")
    await message.answer("Данные получены!")

# Функция для запуска бота
async def start_bot():
    await dp.start_polling(bot)

# Создаем приложение aiohttp для обработки веб-хуков
app = web.Application()

# Получаем порт из переменной окружения (Railway автоматически устанавливает PORT)
port = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    logging.info(f"Запуск бота на порту {port}")
    
    # Запускаем бота в режиме long polling
    import asyncio
    
    # Создаем и запускаем event loop
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    
    # Запускаем веб-сервер
    web.run_app(app, host='0.0.0.0', port=port) 