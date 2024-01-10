from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def not_subs_channels(channels):
    markup = InlineKeyboardMarkup()
    for channel in channels:
        button = InlineKeyboardButton(text=channel[1], url=channel[2])
        markup.row(button)
    check = InlineKeyboardButton(text="Tekshirish", callback_data="check_sub")
    markup.row(check)
    return markup