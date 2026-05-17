import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, ADMIN_TOKEN
from database import db_create
from handlers import router
from admin_handlers import admin_router

async def main():
    db_create()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    admin_bot = Bot(token=ADMIN_TOKEN)
    admin_dp = Dispatcher(storage=MemoryStorage())
    admin_dp.include_router(admin_router)

    print("Botlar ishga tushdi...")

    await asyncio.gather(
        dp.start_polling(bot, allowed_updates=["message"]),
        admin_dp.start_polling(admin_bot, allowed_updates=["message"])
    )

if __name__ == "__main__":
    asyncio.run(main())