from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


for_buyurtma_berish = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚖 Yetkazib berish"), KeyboardButton(text='🏃 Olib ketish')],
        [KeyboardButton(text='⬅️ Orqaga')]
    ],
    resize_keyboard=True
)


barcha_filiallar = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⬅️ Orqaga'), KeyboardButton(text='▶️ Oldinga')],
        [KeyboardButton(text='MAX WAY AVIASOZLAR'), KeyboardButton(text='MAX WAY RISOVIY')]
    ]
)


yetkazib_berish_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Lokatsiya yuborish', request_location=True)],
        [KeyboardButton(text='⬅️ Orqaga')]
    ]
) 
