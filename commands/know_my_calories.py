import config
import main
import utils

from math import ceil
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from config import Form

router = Router()


class Cpfc(StatesGroup):
    calories = State()
    proteins = State()
    fats = State()
    carbs = State()


def set_keyboard(buttons):
    builder = InlineKeyboardBuilder()
    for txt, data in buttons.items():
        builder.button(text=txt, callback_data=data)
    builder.adjust(2)
    return builder.as_markup()


@router.message(Command("set_activ_coef"))
async def set_activ_coef(message: types.Message, state: FSMContext):
    await utils.load_last_user_data(message.from_user.id, state)
    await state.set_state(Form.activ_coef)
    await message.answer(
        text="Выберите уровень активности:"
             "\n\n***1,2*** - минимальная активность (отсутствие физических нагрузок,"
             " сидячая работа, минимум движения)"
             "\n\n***1,375*** - небольшая активность (легкие тренировки или прогулки,"
             " небольшая дневная активность в течение дня)"
             "\n\n***1,46*** - средняя активность (тренировки 4-5 раз в неделю,"
             " хорошая активность в течение дня)"
             "\n\n***1,55*** - активность выше среднего (интенсивные тренировки 5-6 раз в неделю,"
             " хорошая активность в течение дня)"
             "\n\n***1,64*** - повышенная активность (ежедневные тренировки,"
             " высокая дневная активность)"
             "\n\n***1,72*** - высокая активность (ежедневные ультра-интенсивные тренировки"
             " и высокая дневная активность)"
             "\n\n***1,9*** - очень высокая активность (обычно речь идет о спортсменах"
             " в период соревновательной активности)",
        reply_markup=set_keyboard(
            {
                '1,2': '1.2',
                '1,375': '1.375',
                '1,46': '1.46',
                '1,55': '1.55',
                '1,64': '1.64',
                '1,72': '1.72',
                '1,9': '1.9'
            }
        ),
        parse_mode='markdown'
    )


@router.callback_query(Form.activ_coef)
async def _set_activ_coef(call: types.CallbackQuery, state: FSMContext):
    cur_user_data = await state.update_data(activ_coef=call.data)
    utils.set_new_user_data(cur_user_data, call.from_user.id)
    await state.clear()
    await call.message.edit_text("Оки")
    await call.answer()


@router.message(Command("set_aim"))
async def set_aim(message: types.Message):
    await message.answer("Что желаете?",
                         reply_markup=set_keyboard(
                             {
                                 'Похудеть': 'less',
                                 'Держать вес': 'same',
                                 'Набрать массу': 'more',
                                 'Свои значения': 'own'
                             }
                         ))


def get_aim(user_id, coef, _p, _f, _c):
    new_aim = {}
    user_data = utils.get_user_info_as_dict(user_id)
    basic_meta = 9.99 * float(user_data['weight']) + 6.25 * float(user_data['height']) - 4.92 * float(user_data['age'])
    if user_data['gender'] == 'Женский':
        basic_meta -= 161
    else:
        basic_meta += 5
    new_aim['proteins'] = ceil(basic_meta * float(user_data['activ_coef']) * coef * _p / 4)
    new_aim['fats'] = ceil(basic_meta * float(user_data['activ_coef']) * coef * _f / 9)
    new_aim['carbs'] = ceil(basic_meta * float(user_data['activ_coef']) * coef * _c / 4)
    new_aim['calories'] = (new_aim['proteins'] + new_aim['carbs']) * 4 + new_aim['fats'] * 9
    return new_aim


@router.callback_query(F.data == 'less')
async def set_less(call: types.CallbackQuery):
    new_aim = get_aim(call.from_user.id, 0.8, 0.3, 0.3, 0.4)
    await call.message.edit_text(f"Ваша новая цель:"
                                 f"\nКалории: {new_aim['calories']}"
                                 f"\nБелки: {new_aim['proteins']}"
                                 f"\nЖиры: {new_aim['fats']}"
                                 f"\nУглеводы: {new_aim['carbs']}")
    utils.set_user_aim(new_aim, call.from_user.id)
    await call.answer()


@router.callback_query(F.data == 'same')
async def set_same(call: types.CallbackQuery):
    new_aim = get_aim(call.from_user.id, 1, 0.3, 0.3, 0.4)
    await call.message.edit_text(f"Ваша новая цель:"
                                 f"\nКалории: {new_aim['calories']}"
                                 f"\nБелки: {new_aim['proteins']}"
                                 f"\nЖиры: {new_aim['fats']}"
                                 f"\nУглеводы: {new_aim['carbs']}")
    utils.set_user_aim(new_aim, call.from_user.id)
    await call.answer()


@router.callback_query(F.data == 'more')
async def set_more(call: types.CallbackQuery):
    new_aim = get_aim(call.from_user.id, 1.2, 0.35, 0.25, 0.4)
    await call.message.edit_text(f"Ваша новая цель:"
                                 f"\nКалории: {new_aim['calories']}"
                                 f"\nБелки: {new_aim['proteins']}"
                                 f"\nЖиры: {new_aim['fats']}"
                                 f"\nУглеводы: {new_aim['carbs']}")
    utils.set_user_aim(new_aim, call.from_user.id)
    await call.answer()


@router.callback_query(F.data == 'own')
async def set_own(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Установитe количество(г на кг веса) белков')
    await state.set_state(Cpfc.proteins)
    await call.answer()


def normalize(coef):
    if coef.startswith(' '):
        pos = 0
        while coef[pos] == ' ':
            pos += 1
        coef = coef[pos:]
    if len(coef) > 4:
        coef = coef[:4]
    coef.replace(',', '.')
    return coef


@router.message(Cpfc.proteins)
async def set_proteins(message: types.Message, state: FSMContext):
    await state.update_data(proteins=normalize(message.text))
    await state.set_state(Cpfc.fats)
    await message.answer('Установитe количество(г на кг веса) жиров')


@router.message(Cpfc.fats)
async def set_fats(message: types.Message, state: FSMContext):
    await state.update_data(fats=normalize(message.text))
    await state.set_state(Cpfc.carbs)
    await message.answer('Установитe количество(г на кг веса) углеводов')


@router.message(Cpfc.carbs)
async def set_carbs(message: types.Message, state: FSMContext):
    new_aim = await state.update_data(carbs=normalize(message.text))
    await state.clear()
    cur_user_data = utils.get_user_info_as_dict(message.from_user.id)
    for key in new_aim.keys():
        new_aim[key] = ceil(float(new_aim[key]) * float(cur_user_data['weight']))
    new_aim['calories'] = (new_aim['proteins'] + new_aim['carbs']) * 4 + new_aim['fats'] * 9
    utils.set_user_aim(new_aim, message.from_user.id)
    await main.show_user_aim(message)
