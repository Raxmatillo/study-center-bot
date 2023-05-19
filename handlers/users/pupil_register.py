import pandas as pd
import sqlite3
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import AdminFilter
from keyboards.default.menu_keyboards import group_keyboards, block_keyboards, menu
from keyboards.inline.inline_keyboards import confirmation_keyboard

from loader import dp, db


from aiogram.dispatcher.filters.state import State, StatesGroup

class PupilState(StatesGroup):
    group = State()
    block_1 = State()
    block_2 = State()
    full_name = State()
    payment = State()
    confirm = State()



@dp.message_handler(AdminFilter(), text="📊 Excel")
async def send_excel(message: types.Message):
    conn = sqlite3.connect('data/main.db')
    df = pd.read_sql_query("SELECT group_type, block_1, block_2, full_name, payment FROM users", conn)
    df.columns = ['Gurux', 'Blok 1', 'Blok 2', 'To\'liq ism', 'To\'lov']
    df.to_excel('data.xlsx', index=False)
    file = types.InputFile("data.xlsx")

    date = datetime.now()
    await message.answer_document(document=file, caption=f"{date.hour}:{date.minute}\t{date.day}/{date.month}/{date.year}")


@dp.message_handler(AdminFilter(), text="📝 Registratsiya")
async def register_user(message: types.Message):
    markup = await group_keyboards()
    await message.answer("Gurux tanlang", reply_markup=markup)
    await PupilState.group.set()

@dp.message_handler(AdminFilter(), state=PupilState.group, content_types='text')
async def get_group(message: types.Message, state: FSMContext):
    groups = db.get_groups()
    for group in groups:
        print(group[1], message.text, '--------------------')
        if group[1] == message.text:
            await state.update_data(group=message.text)
            markup = await block_keyboards()
            await message.answer("1-blokni tanlang", reply_markup=markup)
            await PupilState.block_1.set()
            break
    else:
        await message.answer("❗️ Iltimos, quyidagilardan birini tanlang!")



@dp.message_handler(AdminFilter(), state=PupilState.block_1, content_types='text')
async def get_block_1(message: types.Message, state: FSMContext):
    blocks = db.get_blocks()
    for block in blocks:
        if block[1] == message.text:
            await state.update_data(block_1=message.text)
            await message.answer("2-blokni tanlang")
            await PupilState.block_2.set()
            break
    else:
        await message.answer("❗️ Iltimos, quyidagilardan birini tanlang!")


@dp.message_handler(AdminFilter(), state=PupilState.block_2, content_types='text')
async def get_block_1(message: types.Message, state: FSMContext):
    blocks = db.get_blocks()
    for block in blocks:
        if block[1] == message.text:
            await state.update_data(block_2=message.text)
            await message.answer("To'liq ismini kiriting", reply_markup=types.ReplyKeyboardRemove())
            await PupilState.full_name.set()
            break
    else:
        await message.answer("❗️ Iltimos, quyidagilardan birini tanlang!")


@dp.message_handler(AdminFilter(), state=PupilState.full_name, content_types='text')
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("To'lovni kiriting")
    await PupilState.payment.set()


@dp.message_handler(AdminFilter(), state=PupilState.payment, content_types='text')
async def get_payment(message: types.Message, state: FSMContext):
    await state.update_data(payment=message.text)

    async with state.proxy() as data:
        group = data.get("group")
        block_1 = data.get("block_1")
        block_2 = data.get("block_2")
        full_name = data.get("full_name")
        payment =  data.get("payment")
    info = "<b>Qabul qilingan ma'lumotlar</b>\n\n"
    info += f"Guruxi: {group}\n"
    info += f"Blok 1: {block_1}\n"
    info += f"Blok 2: {block_2}\n"
    info += f"To'liq ismi: {full_name}\n"
    info += f"To'lov: {payment}"
    await message.answer(text=info, reply_markup=confirmation_keyboard)
    await PupilState.confirm.set()


import openpyxl
@dp.callback_query_handler(AdminFilter(), state=PupilState.confirm, text='confirm')
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_reply_markup()
    async with state.proxy() as data:
        group = data.get("group")
        block_1 = data.get("block_1")
        block_2 = data.get("block_2")
        full_name = data.get("full_name")
        payment = data.get("payment")
    try:
        db.add_user(
            group_type=group,
            block_1=block_1,
            block_2=block_2,
            full_name=full_name,
            payment=payment
        )
        await call.message.answer("✅ Barcha ma'lumotlar qabul qilindi!", reply_markup=menu)
    except Exception as err:
        print(err)
        await call.message.answer("❗️ Bazaga saqlashda xatolik")
    finally:
        await state.finish()

@dp.callback_query_handler(AdminFilter(), state=PupilState.confirm, text='unconfirm')
async def unconfirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("❗️ Bekor qilindi", reply_markup=menu)
    await state.finish()

@dp.message_handler(AdminFilter(), state=PupilState.confirm)
async def unknown__confirm(message: types.Message, state: FSMContext):
    await message.answer("❗️ Iltimos, amalni bajaring!")



@dp.message_handler(AdminFilter(), state=PupilState.group, content_types='any')
@dp.message_handler(AdminFilter(), state=PupilState.block_2, content_types='any')
@dp.message_handler(AdminFilter(), state=PupilState.block_1, content_types='any')
@dp.message_handler(AdminFilter(), state=PupilState.full_name, content_types='any')
@dp.message_handler(AdminFilter(), state=PupilState.payment, content_types='any')
async def unknown__get_block_1(message: types.Message, state: FSMContext):
    await message.answer("❗️ Iltimos, amalni bajaring!")
