from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
# new
from aiogram.filters import Command

from loader import dp, db, ADMIN, bot
from states.admin_states import AdminState, AddProductState

from keyboards.inline.categories_kb import make_categories_inline


@dp.message(Command(commands=['add_category']), F.from_user.id == ADMIN)
async def admin_funtion(message: Message, state: FSMContext):
    await message.answer('Kategoriya nomini kiriting!')
    await state.set_state(AdminState.add_category)


@dp.message(AdminState.add_category, F.from_user.id == ADMIN)
async def add_to_category(message: Message, state: FSMContext):
    text = message.text
    db.add_category(text)
    await state.clear()


@dp.message(Command(commands=['add_vacancy']), F.from_user.id == ADMIN)
async def admin_funtion_vacancy(message: Message, state: FSMContext):
    await message.answer('Vacancy nomini kiriting!')
    await state.set_state(AdminState.add_vacancy)


@dp.message(AdminState.add_vacancy, F.from_user.id == ADMIN)
async def add_to_vacancy(message: Message, state: FSMContext):
    text = message.text
    db.add_vacancy(text)
    await state.clear()


@dp.message(Command(commands=['add_product']), F.from_user.id == ADMIN)
async def add_product_handler(message: Message, state: FSMContext):
    await message.answer('Kategoriyalar:', reply_markup=make_categories_inline())
    
    await state.set_state(AddProductState.category)


@dp.callback_query(F.from_user.id == ADMIN, AddProductState.category)
async def product_category_handler(call: CallbackQuery, state: FSMContext):
    category = call.data
    await state.update_data(category=category)
    await call.message.answer("Mahsulot nomini kiriting")

    await call.message.delete()

    await state.set_state(AddProductState.name)


@dp.message(F.from_user.id == ADMIN, AddProductState.name)
async def product_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer("Mahsulot tavsifini kiriting")
    await state.set_state(AddProductState.description)


@dp.message(F.from_user.id == ADMIN, AddProductState.description)
async def product_description_handler(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)

    await message.answer("Mahsulot narxini kiriting")
    await state.set_state(AddProductState.price)


@dp.message(F.from_user.id == ADMIN, AddProductState.price)
async def product_price_handler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)

    await message.answer("Mahsulot rasmini kiriting")
    await state.set_state(AddProductState.image)


@dp.message(F.content_type.in_({'photo'}), F.from_user.id == ADMIN, AddProductState.image)
async def rasm_handler(message: Message, state: FSMContext):
    
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path
    destination = file_path.replace('photos', 'pictures')
    await bot.download_file(file_path=file_path, destination=destination)
    print(file_id, file_path, file)

    data = await state.get_data()
    category = data.get('category')   
    name = data.get('name') 
    description = data.get('description')
    price = data.get('price')

    db.add_product(
        name=name,
        description=description,
        price=price,
        image=destination,
        category_id=int(category)
        )
    
    await message.answer("Mahsulot bazaga qo'shildi")
    await state.clear()
