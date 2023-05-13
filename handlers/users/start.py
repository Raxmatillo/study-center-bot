import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import AdminFilter

from data.config import ADMINS
from keyboards.default.menu_keyboards import menu
from loader import dp, db, bot


@dp.message_handler(CommandStart(), AdminFilter())
async def bot_start_admin(message: types.Message):
    await message.answer("Xush kelibsiz!", reply_markup=menu)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("O'quv markaz haqida ma'lumot!")