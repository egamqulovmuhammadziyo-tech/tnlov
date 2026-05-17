from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database import natijalar

admin_router = Router()

@admin_router.message(Command("start"))
async def admin_start(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📊 Umumiy ovozlar")]],
        resize_keyboard=True
    )
    await message.answer("👋 Admin panel", reply_markup=markup)

@admin_router.message(F.text == "📊 Umumiy ovozlar")
async def umumiy_ovozlar(message: Message):
    data = natijalar()
    if not data:
        await message.answer("Hali ovoz berilmagan.")
        return

    umumiy = sum(son for _, son in data)

    text = "📊 Umumiy ovozlar:\n\n"
    for i, (ustoz, son) in enumerate(data, 1):
        foiz = round((son / umumiy) * 100, 1)
        text += f"{i}. {ustoz} — {son} ovoz ({foiz}%)\n"

    text += f"\n👥 Jami: {umumiy} ovoz"
    text += f"\n🏆 Lider: {data[0][0]} — {data[0][1]} ovoz"

    await message.answer(text)