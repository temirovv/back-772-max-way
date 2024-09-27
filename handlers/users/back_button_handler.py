from aiogram.types import Message
from loader import dp
from aiogram import F

from aiogram.fsm.context import FSMContext

from states.level_states import BuyurtmaBerishState, FiliallarState
from keyboards.default.second_level_btns import yetkazib_berish_kb, for_buyurtma_berish
from keyboards.default.start_menu import menu


@dp.message(F.text == '⬅️ Orqaga', FiliallarState.choose_filial)
async def back_from_choose_branch(message: Message, state: FSMContext):
    text = "Buyurtma berishni boshlash uchun 🛍 Buyurtma berish tugmasini bosing\n\nShuningdek, aksiyalarni ko'rishingiz va bizning filiallar bilan tanishishingiz mumkin"
    await message.answer(text, reply_markup=menu)
    await state.clear()


@dp.message(F.text == '⬅️ Orqaga', BuyurtmaBerishState.yetkazib_berish)
async def back_from_yetkazib_berish(message: Message, state: FSMContext):
    await message.answer('Yetkazib berish turini tanlang', reply_markup=for_buyurtma_berish)
    await state.clear()


@dp.message(F.text == '⬅️ Orqaga')
async def back_button_handler(message: Message, state: FSMContext):
    await state.clear()
    text = "Buyurtma berishni boshlash uchun 🛍 Buyurtma berish tugmasini bosing\n\nShuningdek, aksiyalarni ko'rishingiz va bizning filiallar bilan tanishishingiz mumkin"
    await message.answer(text, reply_markup=menu)
