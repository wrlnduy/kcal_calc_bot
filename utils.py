import json
import os
import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import defaultForm, defaultAim
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)

def new_user(user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "data.json")
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as data:
            json.dump(defaultForm, data)
    path = os.path.join(path, "aim.json")
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as data:
            json.dump(defaultAim, data)


def get_user_info_as_dict(user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "data.json")
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as data:
            json.dump(defaultForm, data)
    with open(path, "r", encoding='utf-8') as data_json:
        data = json.load(data_json)
    return data


def get_user_info_as_str(user_id):
    user_data = get_user_info_as_dict(user_id)
    for attr, value in defaultForm.items():
        if attr not in user_data.keys():
            user_data[attr] = value
    text = f"Имя: {user_data['name']}"
    text += f"\nПол: {user_data['gender']}"
    text += f"\nВозраст: {user_data['age']}"
    text += f"\nВес: {user_data['weight']}"
    text += f"\nРост: {user_data['height']}"
    text += f"\nСредняя продолжительность сна: {user_data['avg_sleep_len']}"
    text += f"\nКоэффициент активности: {user_data['activ_coef']}"
    return text


async def load_last_user_data(user_id, state: FSMContext):
    data = get_user_info_as_dict(user_id)
    if 'name' in data.keys():
        await state.update_data(name=data['name'])
    else:
        logger.error(f"{user_id} name is lost")
    if 'gender' in data.keys():
        await state.update_data(gender=data['gender'])
    else:
        logger.error(f"{user_id} gender is lost")
    if 'age' in data.keys():
        await state.update_data(age=data['age'])
    else:
        logger.error(f"{user_id} age is lost")
    if 'weight' in data.keys():
        await state.update_data(weight=data['weight'])
    else:
        logger.error(f"{user_id} weight is lost")
    if 'height' in data.keys():
        await state.update_data(height=data['height'])
    else:
        logger.error(f"{user_id} height is lost")
    if 'avg_sleep_len' in data.keys():
        await state.update_data(avg_sleep_len=data['avg_sleep_len'])
    else:
        logger.error(f"{user_id} sleep_len is lost")
    if 'activ_coef' in data.keys():
        await state.update_data(activ_coef=data['activ_coef'])
    else:
        logger.error(f"{user_id} activity_coefficient is lost")


def set_new_user_data(new_user_data, user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "data.json")
    with open(path, "w", encoding='utf-8') as data:
        json.dump(new_user_data, data)


def get_user_aim_as_dict(user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "aim.json")
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as data:
            json.dump(defaultForm, data)
    with open(path, "r", encoding='utf-8') as data_json:
        data = json.load(data_json)
    return data


def set_user_aim(new_aim, user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "aim.json")
    with open(path, 'w', encoding='utf-8') as data:
        json.dump(new_aim, data)


def get_user_aim_as_str(user_id):
    user_aim = get_user_aim_as_dict(user_id)
    for attr, value in defaultAim.items():
        if attr not in user_aim.keys():
            user_aim[attr] = value
    text = f"Калории: {user_aim['calories']}"
    text += f"\nБелки: {user_aim['proteins']}"
    text += f"\nЖиры: {user_aim['fats']}"
    text += f"\nУглеводы: {user_aim['carbs']}"
    return text


def set_keyboard(buttons):
    builder = InlineKeyboardBuilder()
    for txt, data in buttons.items():
        builder.button(text=txt, callback_data=data)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


# добавление блюд в список
# def add_new_dish(dish_data):
