from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import ovoz_bergan, ovoz_saqlash, natijalar
from admin import admin_ga_yuborish
from config import USTOZLAR

router = Router()

def ovoz_markup():
    tugmalar = [[KeyboardButton(text=ustoz)] for ustoz in USTOZLAR]
    return ReplyKeyboardMarkup(keyboard=tugmalar, resize_keyboard=True)

@router.message(Command("start"))
async def start(message: Message):
    if ovoz_bergan(message.from_user.id):
        await message.answer("❌ Siz allaqachon ovoz bergansiz!")
        return
    await message.answer("🗳 Xush kelibsiz! Kimga ovoz berasiz?", reply_markup=ovoz_markup())

@router.message(F.text.in_(USTOZLAR))
async def ovoz_qabul(message: Message):
    user_id = message.from_user.id

    if ovoz_bergan(user_id):
        await message.answer("❌ Siz allaqachon ovoz bergansiz!")
        return

    ovoz_saqlash(user_id, message.text)
    await message.answer(
        f"✅ Ovozingiz qabul qilindi!\n👨‍🏫 Ustoz: {message.text}",
        reply_markup=ReplyKeyboardRemove()
    )

    data = natijalar()
    text = "📊 Joriy natijalar:\n\n"
    for i, (ustoz, son) in enumerate(data, 1):
        text += f"{i}. {ustoz} — {son} ovoz\n"
    text += f"\n🏆 Hozircha lider: {data[0][0]} — {data[0][1]} ovoz"
    admin_ga_yuborish(text)

@router.message(Command("natija"))
async def natija(message: Message):
    data = natijalar()
    if not data:
        await message.answer("Hali ovoz berilmagan.")
        return

    text = "📊 Yakuniy natijalar:\n\n"
    for i, (ustoz, son) in enumerate(data, 1):
        text += f"{i}. {ustoz} — {son} ovoz\n"
    text += f"\n🏆 G'olib: {data[0][0]} — {data[0][1]} ovoz"

    await message.answer(text)
    admin_ga_yuborish(text)