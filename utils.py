import json
import os

from config import defaultForm
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


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
    text = f"Имя: {user_data['name']}"
    text += f"\nПол: {user_data['gender']}"
    text += f"\nВозраст: {user_data['age']}"
    text += f"\nВес: {user_data['weight']}"
    text += f"\nРост: {user_data['height']}"
    text += f"\nСредняя продолжительность сна: {user_data['avg_sleep_len']}"
    return text


def new_user(user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "data.json")
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as data:
            json.dump(defaultForm, data)


async def load_last_user_data(user_id, state: FSMContext):
    data = get_user_info_as_dict(user_id)
    await state.update_data(name=data['name'])
    await state.update_data(gender=data['gender'])
    await state.update_data(age=data['age'])
    await state.update_data(weight=data['weight'])
    await state.update_data(height=data['height'])
    await state.update_data(avg_sleep_len=data['avg_sleep_len'])


def set_new_user_data(new_user_data, user_id):
    path = os.path.join("users", str(user_id))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "data.json")
    with open(path, "w", encoding='utf-8') as data:
        json.dump(new_user_data, data)
