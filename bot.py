import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота и URL приложения
BOT_TOKEN = "8039344227:AAEDCP_902a3r52JIdM9REqUyPx-p2IVtxA"
WEBAPP_URL = "https://testos-production.up.railway.app"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем веб-приложение
app = web.Application()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🔍 Открыть анонимный чат",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
    )
    
    welcome_text = (
        "👋 Добро пожаловать в Анонимный Чат!\n\n"
        "🔒 Здесь вы можете общаться анонимно и безопасно.\n"
        "👤 Найдите собеседника по интересам\n"
        "🔄 Меняйте собеседника одним нажатием\n\n"
        "Нажмите кнопку ниже, чтобы начать общение 👇"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)

@dp.message()
async def handle_message(message: types.Message):
    if message.web_app_data:
        try:
            logging.info(f"Получены данные: {message.web_app_data.data}")
            await message.answer("✅ Данные успешно получены!")
        except Exception as e:
            logging.error(f"Ошибка при обработке данных: {e}")
            await message.answer("❌ Произошла ошибка при обработке данных")
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔍 Открыть чат",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )]
            ]
        )
        await message.answer("Используйте кнопку ниже для доступа к чату:", reply_markup=keyboard)

async def on_startup(app):
    # Запускаем бота при старте приложения
    asyncio.create_task(dp.start_polling(bot, skip_updates=True))

if __name__ == '__main__':
    # Настраиваем и запускаем приложение
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=3000) 