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

# Настройка статических файлов
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# Добавляем маршрут для статических файлов
app.router.add_static('/', static_dir, show_index=True)

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

# Обработчик для получения данных из веб-приложения
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

async def start_bot():
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

async def on_startup(app):
    # Запускаем бота при старте приложения
    asyncio.create_task(start_bot())

if __name__ == '__main__':
    # Получаем порт из переменной окружения
    port = int(os.getenv('PORT', 8080))
    
    logging.info(f"Запуск приложения на порту {port}")
    
    # Добавляем обработчик запуска
    app.on_startup.append(on_startup)
    
    # Запускаем веб-сервер
    web.run_app(app, host='0.0.0.0', port=port) 