from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Registratsiya"),
            KeyboardButton(text="Excel")
        ]
    ], resize_keyboard=True
)


async def group_keyboards():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    groups = db.get_groups()

    for group in groups:
        markup.insert(
            KeyboardButton(text=group[1])
        )

    return markup


async def block_keyboards():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    blocks = db.get_blocks()
    for block in blocks:
        markup.insert(
            KeyboardButton(text=block[1])
        )

    return markup