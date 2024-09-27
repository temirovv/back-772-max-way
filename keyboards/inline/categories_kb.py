from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db


def make_categories_inline():
    menu = InlineKeyboardBuilder()
    menu.max_width = 2

    inline_buttons = []
    categories = db.get_categories_for_admin()

    for category in categories:
        category_id, name = category
        button = InlineKeyboardButton(text=name, callback_data=str(category_id))
        inline_buttons.append(button)
    
    menu.row(*inline_buttons)

    return menu.as_markup()



