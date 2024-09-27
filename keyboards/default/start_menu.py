from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🛍 Buyurtma berish')],
        [KeyboardButton(text='🎉 Aksiya'), KeyboardButton(text='🏘 Barcha filiallar')],
        [KeyboardButton(text='💼 Vakansiyalar'), KeyboardButton(text="ℹ️ Biz haqimizda")],
    ],
    resize_keyboard=True
)

