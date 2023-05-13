from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='confirm'),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data='unconfirm')
        ]
    ], row_width=2
)