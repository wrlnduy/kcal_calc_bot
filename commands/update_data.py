import utils
import logging

from datetime import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from utils import load_last_user_data, set_new_user_data

router = Router()
logger = logging.getLogger(__name__)


def set_digits_keyboard(attr, alr):
    kb = InlineKeyboardBuilder()
    for digit in range(0, 10):
        kb.button(
            text=str(digit),
            callback_data='UPD' + attr + alr + str(digit)
        )
    kb.button(
        text='.',
        callback_data="UPD" + attr + alr + '.'
    )
    kb.button(
        text='⌫',
        callback_data='ERD' + attr + alr
    )
    kb.button(
        text='✅',
        callback_data='AC' + attr + alr
    )
    kb.button(
        text='🚫',
        callback_data='WA' + attr
    )
    kb.adjust(8, 4)
    return kb.as_markup()


def set_lowercase_letter_keyboard(attr, alr):
    kb = InlineKeyboardBuilder()
    for letter in "йцукенгшщзхъфывапролджэячсмитьбю":
        kb.button(
            text=letter,
            callback_data='UPL' + attr + alr + letter
        )
    kb.button(
        text='⌫',
        callback_data='ERL' + attr + alr
    )
    kb.button(
        text='⬆️',
        callback_data='UU' + attr + alr
    )
    kb.button(
        text='✅',
        callback_data='AC' + attr + alr
    )
    kb.button(
        text='🚫',
        callback_data='WA' + attr
    )
    kb.adjust(8)
    return kb.as_markup()


@router.callback_query(F.data.startswith("UL"))
async def lowercase_letter_keyboard(call: CallbackQuery):
    attr = call.data[2:]
    if len(attr) > 2:
        attr = attr[:4 - len(call.data)]
    alr = call.data[4:]

    kb = InlineKeyboardBuilder()
    for letter in "йцукенгшщзхъфывапролджэячсмитьбю":
        kb.button(
            text=letter,
            callback_data='UPL' + attr + alr + letter
        )
    kb.button(
        text='⌫',
        callback_data='ERL' + attr + alr
    )
    kb.button(
        text='⬆️',
        callback_data='UU' + attr + alr
    )
    kb.button(
        text='✅',
        callback_data='AC' + attr + alr
    )
    kb.button(
        text='🚫',
        callback_data='WA' + attr
    )
    kb.adjust(8)

    await call.message.edit_text(
        alr + "_",
        reply_markup=kb.as_markup()
    )
    await call.answer()


@router.callback_query(F.data.startswith("UU"))
async def uppercase_letter_keyboard(call: CallbackQuery):
    attr = call.data[2:]
    if len(attr) > 2:
        attr = attr[:4 - len(call.data)]
    alr = call.data[4:]

    kb = InlineKeyboardBuilder()
    for letter in "ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТЬБЮ":
        kb.button(
            text=letter,
            callback_data='UPL' + attr + alr + letter
        )
    kb.button(
        text='⌫',
        callback_data='ERL' + attr + alr
    )
    kb.button(
        text='⬆️',
        callback_data='UL' + attr + alr
    )
    kb.button(
        text='✅',
        callback_data='AC' + attr + alr
    )
    kb.button(
        text='🚫',
        callback_data='WA' + attr
    )
    kb.adjust(8, 8, 8, 7)

    await call.message.edit_text(
        alr + "_",
        reply_markup=kb.as_markup()
    )
    await call.answer()


def set_keyboard(buttons):
    builder = InlineKeyboardBuilder()
    for txt, data in buttons.items():
        builder.button(text=txt, callback_data=data)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


@router.message(Command("update_data"))
async def update_user_data(message: types.Message, state: FSMContext):
    await load_last_user_data(message.from_user.id, state)
    text = '```\n'
    text += utils.get_user_info_as_str(message.from_user.id)
    text += '\n```'
    await message.answer(
        text,
        reply_markup=set_keyboard(
            {
                'Имя': 'UPLNA',
                'Пол(м/ж)': 'UPLGE',
                'Возраст(полных лет)': 'UPDAG',
                'Вес': 'UPDWE',
                'Рост(см)': 'UPDHE',
                'Средняя продолжительность сна': 'UPDAV',
                '🛑Закончить🛑': 'cancel'
            }
        ),
        parse_mode='markdown'
    )


async def update_user_data(call: CallbackQuery):
    text = '```\n'
    text += utils.get_user_info_as_str(call.from_user.id)
    text += '\n```'
    await call.message.edit_text(
        text,
        reply_markup=set_keyboard(
            {
                'Имя': 'UPLNA',
                'Пол(м/ж)': 'UPLGE',
                'Возраст(полных лет)': 'UPDAG',
                'Вес': 'UPDWE',
                'Рост(см)': 'UPDHE',
                'Средняя продолжительность сна': 'UPDAV',
                '🛑Закончить🛑': 'cancel'
            }
        ),
        parse_mode='markdown'
    )
    await call.answer()


@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    logger.info(f'{call.from_user.id} successfully changed data')
    await state.clear()
    await call.message.edit_text("Изменения в силе")
    await call.answer()


@router.callback_query(F.data.startswith("WA"))
async def not_this_one(call: CallbackQuery):
    await update_user_data(call)


@router.callback_query(F.data.startswith("ER"))
async def backspace(call: CallbackQuery):
    attr_type = call.data[2:][0]
    attr = call.data[3:]
    if len(attr) > 2:
        attr = attr[:5 - len(call.data)]
    cur_state = call.data[5:]
    if len(cur_state) == 0:
        await call.answer("Нечего удалять")
        return
    cur_state = cur_state[:-1]
    if attr_type == 'D':
        await call.message.edit_text(
            cur_state + "_",
            reply_markup=set_digits_keyboard(attr, cur_state)
        )
    else:
        await call.message.edit_text(
            cur_state + "_",
            reply_markup=set_lowercase_letter_keyboard(attr, cur_state)
        )
    await call.answer()


@router.callback_query(F.data.startswith("AC"))
async def set_attr(call: CallbackQuery, state: FSMContext):
    attr = call.data[2:]
    if len(attr) > 2:
        attr = attr[:4 - len(call.data)]
    cur_state = call.data[4:]
    if cur_state == "":
        cur_state = 'Не указано'
    if attr == 'NA':
        cur_user_data = await state.update_data(name=cur_state)
    elif attr == 'GE':
        if cur_state == 'м':
            cur_state = 'Мужской'
        else:
            cur_state = 'Женский'
        cur_user_data = await state.update_data(gender=cur_state)
    elif attr == 'AG':
        cur_user_data = await state.update_data(age=cur_state)
    elif attr == 'WE':
        cur_user_data = await state.update_data(weight=cur_state)
    elif attr == 'HE':
        cur_user_data = await state.update_data(height=cur_state)
    else:
        cur_user_data = await state.update_data(avg_sleep_len=cur_state)
    set_new_user_data(cur_user_data, call.from_user.id)
    await update_user_data(call)


@router.callback_query(F.data.startswith("UP"))
async def update(call: CallbackQuery):
    attr_type = call.data[2:][0]
    attr = call.data[3:]
    if len(attr) > 2:
        attr = attr[:5 - len(call.data)]
    cur_state = call.data[5:]
    if attr_type == 'D':
        await call.message.edit_text(
            cur_state + "_",
            reply_markup=set_digits_keyboard(attr, cur_state)
        )
    else:
        await call.message.edit_text(
            cur_state + "_",
            reply_markup=set_lowercase_letter_keyboard(attr, cur_state)
        )
    await call.answer()
