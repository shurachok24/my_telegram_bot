import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiohttp import web
from threading import Thread
import asyncio

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчики бота
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Бот работает на Fly.io ✅")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

# Health-check endpoint для Fly.io
async def handle_health(request):
    return web.Response(text="OK")

def start_health_server():
    app = web.Application()
    app.router.add_get("/health", handle_health)
    web.run_app(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    # Запускаем health server в отдельном потоке
    Thread(target=start_health_server, daemon=True).start()

    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

