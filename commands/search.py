import datetime

from datetime import datetime
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import utils
from config import food, food_last_page, NUMBER_OF_BUTTONS
from utils import set_keyboard, normalize_float, normalize_str, add_food_to_notepad
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class Query(StatesGroup):
    type = State()
    name = State()
    weight = State()


def levenshtein_distance(a, b):
    if len(a) > len(b):
        a, b = b, a
    row = [0] * (len(a) + 1)
    dp = [row, row. copy()]
    for i in range(0, len(a) + 1):
        dp[0][i] = i
    for i in range(0, len(b)):
        dp[1][0] = i + 1
        for j in range(1, len(a) + 1):
            dp[1][j] = min(dp[0][j] + 1,
                           dp[1][j - 1] + 1,
                           dp[0][j - 1] + (a[j - 1] != b[i]))
        dp[0], dp[1] = dp[1], dp[0]
    return dp[0][len(a)]


def get_sorted_list(cur_food):
    def comp(a):
        return a[0]
    sorted_list = []
    for item in food[cur_food['type']].keys():
        if cur_food['name'] in item.casefold():
            sorted_list.append((0, item))
        else:
            sorted_list.append((levenshtein_distance(cur_food['name'], normalize_str(item)), item))
    sorted_list.sort(key=comp)
    return sorted_list


async def show_page(page: int, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    page_size = min(NUMBER_OF_BUTTONS, len((await state.get_data())['sorted_list']) - page * NUMBER_OF_BUTTONS)
    keyboard.button(text='<<<', callback_data='SW' + str(page - 5))
    keyboard.button(text='<', callback_data='SW' + str(page - 1))
    keyboard.button(text='>', callback_data='SW' + str(page + 1))
    keyboard.button(text='>>>', callback_data='SW' + str(page + 5))
    for i in range(page * NUMBER_OF_BUTTONS, page * NUMBER_OF_BUTTONS + page_size):
        food_name = (await state.get_data())['sorted_list'][i][1]
        keyboard.button(text=food_name, callback_data='AD' + str(i))
    keyboard.adjust(4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return keyboard.as_markup()


@router.message(Command("add_food_to_my_notepad"))
async def choose_category(message: types.Message, state: FSMContext):
    await state.set_state(Query.type)
    await state.update_data(time=datetime.now().strftime("%d-%m-%Y"))
    await message.answer("Из какой категории блюдо ?",
                         reply_markup=set_keyboard(
                             {
                                 'Продукты': 'products',
                                 'Напитки': 'drinks',
                                 'Торты': 'cakes',
                                 'Десерты': 'desserts',
                                 'Вторые блюда': 'garnish',
                                 'Салаты': 'salads',
                                 'Бутерброды': 'sandwiches',
                                 'Соусы': 'sauces',
                                 'Закуски': 'snacks',
                                 'Супы': 'soups'
                             }
                         ))


@router.callback_query(Query.type)
async def add_dish(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(type=call.data)
    await call.message.edit_text("Введите название")
    await state.set_state(Query.name)
    await call.answer()


@router.message(Query.name)
async def show_food(message: types.Message, state: FSMContext):
    cur_food = await state.update_data(name=message.text)
    await state.update_data(name='')
    if cur_food['name'].startswith(' '):
        amount = 0
        while cur_food['name'][amount] == ' ':
            amount += 1
        cur_food['name'] = cur_food['name'][amount:]
    if cur_food['name'].endswith(' '):
        amount = 0
        while cur_food['name'][len(cur_food['name']) - amount - 1]:
            amount += 1
        cur_food['name'] = cur_food['name'][:-amount]
    cur_food['name'] = normalize_str(cur_food['name'])
    await state.update_data(sorted_list=get_sorted_list(cur_food))
    await message.answer("Возможно вы про: ", reply_markup=await show_page(0, state))


@router.callback_query(F.data.startswith('SW'))
async def swap_page(call: types.CallbackQuery, state: FSMContext):
    page = int(call.data[2:])
    if page < 0 or page > food_last_page[(await state.get_data())['type']]:
        await call.answer('Такой страницы нет')
        return
    await call.message.edit_text('Возможно вы про: ', reply_markup=await show_page(page, state))
    await call.answer()


@router.callback_query(F.data.startswith("AD"))
async def know_food_name(call: types.CallbackQuery, state: FSMContext):
    food_id = int(call.data[2:])
    food_name = (await state.get_data())['sorted_list'][food_id][1]
    await state.update_data(sorted_list=None)
    await state.update_data(name=food_name)
    await state.set_state(Query.weight)
    await call.message.edit_text('Введите вес(г)')
    await call.answer()


@router.message(Query.weight)
async def know_food_weight(message: types.Message, state: FSMContext):
    weight = normalize_float(message.text)
    cur_data = await state.get_data()
    await state.clear()
    add_food_to_notepad(message.from_user.id, cur_data['type'], cur_data['name'], weight, cur_data['time'])
    text = ''
    text += '```\n'
    text += utils.get_day_food_data_as_str(message.from_user.id, cur_data['time'])
    text += '\n```'
    await message.answer(text, parse_mode='markdown')
