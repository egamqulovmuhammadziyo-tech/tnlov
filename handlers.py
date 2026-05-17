from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import ovoz_bergan, ovoz_saqlash, natijalar
from config import USTOZLAR, ADMIN_CHAT_ID
from database import ovoz_bergan, ovoz_saqlash, natijalar, reset_ovozlar
router = Router()




def ovoz_markup():
    tugmalar = [[KeyboardButton(text=ustoz)] for ustoz in USTOZLAR]
    return ReplyKeyboardMarkup(keyboard=tugmalar, resize_keyboard=True)

def admin_markup():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📊 Umumiy ovozlar")]],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def start(message: Message):
    # Admin tekshirish
    if str(message.from_user.id) == str(ADMIN_CHAT_ID):
        await message.answer("👋 Admin panel", reply_markup=admin_markup())
        return
def admin_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Umumiy ovozlar")],
            [KeyboardButton(text="🔄 Ovozlarni reset qilish")]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "🔄 Ovozlarni reset qilish")
async def reset_handler(message: Message):
    if str(message.from_user.id) != str(ADMIN_CHAT_ID):
        return

    # Tasdiqlash so'rash
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Ha, reset qilish")],
            [KeyboardButton(text="❌ Yo'q, bekor qilish")]
        ],
        resize_keyboard=True
    )
    await message.answer("⚠️ Hamma ovozlar o'chib ketadi! Davom etasizmi?", reply_markup=markup)

@router.message(F.text == "✅ Ha, reset qilish")
async def reset_tasdiqlash(message: Message):
    if str(message.from_user.id) != str(ADMIN_CHAT_ID):
        return

    reset_ovozlar()
    await message.answer("✅ Barcha ovozlar o'chirildi!", reply_markup=admin_markup())

@router.message(F.text == "❌ Yo'q, bekor qilish")
async def reset_bekor(message: Message):
    if str(message.from_user.id) != str(ADMIN_CHAT_ID):
        return

    await message.answer("❌ Reset bekor qilindi.", reply_markup=admin_markup())
    # Foydalanuvchi
    if ovoz_bergan(message.from_user.id):
        await message.answer("❌ Siz allaqachon ovoz bergansiz!")
        return

    await message.answer("🗳 Xush kelibsiz! Kimga ovoz berasiz?", reply_markup=ovoz_markup())

@router.message(F.text == "📊 Umumiy ovozlar")
async def umumiy_ovozlar(message: Message):
    if str(message.from_user.id) != str(ADMIN_CHAT_ID):
        return

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