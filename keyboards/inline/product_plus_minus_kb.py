from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


def make_product_plus_minus(quantity = 1):
    menu = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(text='➖', callback_data='minus'),
                InlineKeyboardButton(text=f'{quantity}', callback_data=f"quantity.{quantity}"),
                InlineKeyboardButton(text='➕', callback_data='plus')],
            [
                InlineKeyboardButton(text="🛒", callback_data='add_to_cart')
            ],
        ]
    )
    
    return menu.as_markup()


def get_user_cart_sub_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buyurtmani tasdiqlash", callback_data='confirming_order')],
            [InlineKeyboardButton(text='Buyurtmani davom ettirish', callback_data='continue_order')],
            [InlineKeyboardButton(text='♻️ Tozalash', callback_data='clean_cart')]
        ]
    )
