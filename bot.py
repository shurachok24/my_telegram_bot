import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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
    import asyncio
    loop = asyncio.get_event_loop()

    # Запускаем бота и сервер health-check параллельно
    from threading import Thread
    Thread(target=start_health_server, daemon=True).start()

    executor.start_polling(dp, skip_updates=True)
