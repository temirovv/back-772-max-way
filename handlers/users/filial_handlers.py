from aiogram.types import Message
from loader import dp
from aiogram import F

from states.level_states import FiliallarState


@dp.message(F.text == 'MAX WAY AVIASOZLAR', FiliallarState.choose_filial)
async def handler_location1(message: Message):
    text = '📍 Filial:  MAX WAY AVIASOZLAR\n\n🗺 Manzil:  улица Авиасозлар, 23\n\n🏢 Orientir:\n\n☎️ Telefon raqami:  +998712005400\n\n🕙 Ish vaqti : 10:00 - 03:00'
    await message.answer(text)
    await message.answer_location(
        latitude=41.290894,
        longitude=69.342153
    )
