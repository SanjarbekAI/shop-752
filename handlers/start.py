from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.user import user_main_menu, phone_share
from keyboards.inline.user import not_subs_channels
from loader import dp, db_manager
from states.user import RegisterState
from utils.misc.checker import login_def
from utils.misc.subs_checker import check
from data.config import channels

@dp.callback_query_handler(text="check_sub")
async def check_sub_handler(call: types.CallbackQuery):
    not_subs = []
    for channel in channels:
        check_user = await check(user_id=call.message.chat.id, channel=channel[0])
        if not check_user:
            not_subs.append(channel)
    if len(not_subs) == 0:
        user = db_manager.get_user(chat_id=call.message.chat.id)
        if user:
            text = "Botimizga xush kelibsiz."
            await call.message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Iltimos telefon raqamingizni kiriting"
            await call.message.answer(text=text, reply_markup=phone_share)
            await RegisterState.phone_number.set()
    else:
        text = "Ushbu kanllarga a'zo bo'lishing kerak.\n\n"
        for channel in not_subs:
            text += f"<a href='{channel[2]}'>{channel[1]}</a>\n"
        buttons = await not_subs_channels(not_subs)
        await call.message.answer(text=text, reply_markup=buttons)



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    not_subs = []
    for channel in channels:
        check_user = await check(user_id=message.chat.id, channel=channel[0])
        if not check_user:
            not_subs.append(channel)

    if len(not_subs) == 0:
        user = db_manager.get_user(chat_id=message.chat.id)
        if user:
            text = "Botimizga xush kelibsiz."
            await message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Iltimos telefon raqamingizni kiriting"
            await message.answer(text=text, reply_markup=phone_share)
            await RegisterState.phone_number.set()
    else:
        text = "Ushbu kanllarga a'zo bo'lishing kerak.\n\n"
        for channel in not_subs:
            text += f"<a href='{channel[2]}'>{channel[1]}</a>\n"
        buttons = await not_subs_channels(not_subs)
        await message.answer(text=text, reply_markup=buttons)


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    text = "Iltimos, Mars Space uchun mo'jallangan login ni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.login.set()


@dp.message_handler(state=RegisterState.login)
async def get_login_number(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    text = "Iltimos, Mars Space uchun mo'jallangan password ni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.password.set()


@dp.message_handler(state=RegisterState.password)
async def get_password_number(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text, chat_id=message.chat.id)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    student = login_def(login, password)
    if student:
        await state.update_data(full_name=student)
        data = await state.get_data()
        if db_manager.insert_user(data):
            text = f"Tabriklaymiz, siz muvafaqqiyatli ro'yxatdan o'tdingiz ✅ {student}"
            await message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Botda nosozlik mavjud"
            await message.answer(text=text)
    else:
        text = "Notog'ri login yoki password kiritdingiz. Qayta urunish uchun /start bosing"
        await message.answer(text=text)
    await state.finish()