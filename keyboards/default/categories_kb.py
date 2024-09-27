from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from loader import db


def get_categories_kb():
    menu = ReplyKeyboardBuilder()
    menu.max_width = 2

    buttons = []

    for category in db.get_categories_for_admin():
        category_id, category_name = category # (id, name)
        buttons.append(
            KeyboardButton(text=category_name)
        )

    menu.row(*buttons)

    return menu.as_markup(resize_keyboard=True)
