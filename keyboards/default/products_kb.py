from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


def make_products_keyboard(category_name: str) -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)
    buttons = []

    products = db.get_products_by_category(category_name)
    for product in products:
        buttons.append(
            KeyboardButton(text=product[0])
        )

    menu.keyboard.append(buttons)

    return menu


def get_sub_cart_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='⬅️ Orqaga'),
                KeyboardButton(text='🛒 Savat')
            ]
        ]
    )
