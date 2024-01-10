from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

@dp.message_handler(text="🚀 Mars Bozor")
async def mars_bozor_handler(message: types.Message):
    text = "Mars bozorga xush kelibsiz"
    await message.answer(text=text)