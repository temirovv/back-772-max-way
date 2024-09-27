from aiogram.types import Message, FSInputFile, CallbackQuery
from loader import dp, db
from aiogram import F

from aiogram.fsm.context import FSMContext

from keyboards.default.second_level_btns import for_buyurtma_berish, barcha_filiallar
from keyboards.default.second_level_btns import yetkazib_berish_kb
from states.level_states import FiliallarState, BuyurtmaBerishState

from keyboards.inline.vacancy_kb import kurer_menu, operator_menu,tozalik_xodimi_menu, ranner_menu, qadoqlovchi_menu, kassir_menu, oshpaz_menu
from keyboards.default.categories_kb import get_categories_kb
from keyboards.default.products_kb import make_products_keyboard, get_sub_cart_keyboard
from keyboards.inline.product_plus_minus_kb import make_product_plus_minus, get_user_cart_sub_keyboard


@dp.message(F.text == '🛍 Buyurtma berish')
async def buyurtma_berish(message: Message):
    await message.answer("Yetkazib berish turini tanlang", reply_markup=for_buyurtma_berish)

@dp.message(F.text == '🎉 Aksiya')
async def buyurtma_berish(message: Message):
    await message.answer("Hozirgi vaqtda hech qanday aksiyalar yo'q")

@dp.message(F.text == '🏘 Barcha filiallar')
async def barcha_filialllar_handler(message: Message, state: FSMContext):
    await message.answer("Bizning filiallarimiz :", reply_markup=barcha_filiallar)
    await state.set_state(FiliallarState.choose_filial)



@dp.message(F.text == '💼 Vakansiyalar')
async def barcha_filialllar_handler(message: Message, state: FSMContext):
    await message.answer("💼 Vakansiyalar:")
    await message.answer("Kuryer", reply_markup=kurer_menu)
    await message.answer('Operator', reply_markup=operator_menu)
    await message.answer('Tozalik xodimi', reply_markup=tozalik_xodimi_menu)
    await message.answer('Ranner', reply_markup=ranner_menu)
    await message.answer('Qadoqlovchi', reply_markup=qadoqlovchi_menu)
    await message.answer('Kassir', reply_markup=kassir_menu)
    await message.answer('Oshpaz', reply_markup=oshpaz_menu)


@dp.message(F.text == '🚖 Yetkazib berish')
async def yetkazib_berish_handler(message: Message, state: FSMContext):
    await message.answer(
        'Buyurtmani davom ettirish uchun iltimos lokatsiyangizni yuboring',
        reply_markup=yetkazib_berish_kb
        )
    await state.set_state(BuyurtmaBerishState.yetkazib_berish)


@dp.message(BuyurtmaBerishState.yetkazib_berish)
async def location_handler(message: Message, state: FSMContext):
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        await message.answer('Kategoriyalardan birini tanlang', reply_markup=get_categories_kb())
        await state.update_data(
            latitude=latitude, longitude=longitude
        )
        await state.set_state(BuyurtmaBerishState.category)
    else:
        await message.answer('Iltimos lokatsiya yuboring', reply_markup=yetkazib_berish_kb)


@dp.message(BuyurtmaBerishState.category)
async def user_category_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(category=name)
    await message.answer(
        "Mahsulotlardan  birini tanlang", 
        reply_markup=make_products_keyboard(name))
    
    await state.set_state(BuyurtmaBerishState.product)


@dp.message(F.text == '🛒 Savat', BuyurtmaBerishState.product)
async def show_user_cart_handler(message: Message, state: FSMContext):
    user = message.from_user.id
    carts = db.get_user_cart(user=user)

    main_text = ''
    for cart in carts:
        name, price, quantity = cart
        main_text += f"{name} x {quantity} = {quantity*price}\n"

    await message.answer(main_text, reply_markup=get_user_cart_sub_keyboard())


@dp.message(F.text == '⬅️ Orqaga', BuyurtmaBerishState.product)
async def back_to_select_product_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')
    await message.answer(
        "Mahsulotlardan  birini tanlang", 
        reply_markup=make_products_keyboard(category))


@dp.message(BuyurtmaBerishState.product)
async def user_product_handler(message: Message, state: FSMContext):
    product_name = message.text

    name, description, price, image = db.get_product(product_name)
    caption = f"{name}\n{description}\n\n{name} {price} x 1 = {price}\nUmumiy: {price}"

    photo_file = FSInputFile(path=image)
    await message.answer_photo(
        photo=photo_file, 
        caption=caption,
        reply_markup=make_product_plus_minus())
    
    await  state.update_data(
        name=name, description=description,
        price=price, quantity = 1
    )


@dp.callback_query(BuyurtmaBerishState.product, F.data == 'plus')
async def product_plust_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Plus bosildi :)")

    data = await state.get_data()
    quantity = data.get('quantity')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    quantity += 1
    await state.update_data(quantity=quantity)

    jami = price * quantity
    caption = f"{name}\n{description}\n\n{name} {price} x {quantity} = {jami}\nUmumiy: {jami}"

    
    await call.message.edit_caption(caption=caption, reply_markup=make_product_plus_minus(quantity))


@dp.callback_query(BuyurtmaBerishState.product, F.data == 'minus')
async def product_plust_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Minus bosildi :)")

    data = await state.get_data()
    quantity = data.get('quantity')
    
    if quantity != 1:
        quantity -= 1
        await state.update_data(quantity=quantity)

    await call.message.edit_reply_markup(
        reply_markup=make_product_plus_minus(quantity)
    )


@dp.callback_query(BuyurtmaBerishState.product, F.data == 'add_to_cart')
async def add_to_cart_handler(call: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    name = data.get('name')
    quantity = data.get('quantity')
    user = call.from_user.id

    db.add_to_cart(
        product_name=name,
        quantity=quantity,
        user=user
    )

    await call.message.answer("Mahsulot savatga qo'shildi", reply_markup=get_sub_cart_keyboard())
    await call.message.delete()


@dp.callback_query(BuyurtmaBerishState.product, F.data == 'clean_cart')
async def clean_cart_handler(call: CallbackQuery, state: FSMContext):
    tg_id = call.from_user.id
    db.clean_user_cart(user=tg_id)
    data = await state.get_data()
    category = data.get('category')

    await call.message.answer(
        "Mahsulotlardan  birini tanlang", 
        reply_markup=make_products_keyboard(category))
    
    await call.answer('Savat tozalandi')
    await call.message.delete()



@dp.callback_query(BuyurtmaBerishState.product, F.data == 'continue_order')
async def continue_order_handler(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    category = data.get('category')

    await call.message.answer(
        "Mahsulotlardan  birini tanlang", 
        reply_markup=make_products_keyboard(category))
    
    await call.message.delete()
