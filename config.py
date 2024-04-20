import os
import json

from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEMOCRACY_ID = os.getenv("DEMOCRACY_ID")
CHAT_ID = os.getenv("BOT_USERNAME")

defaultForm = {
    'name': 'Не указано',
    'gender': 'Не указано',
    'age': 'Не указано',
    'weight': 'Не указано',
    'height': 'Не указано',
    'avg_sleep_len': 'Не указано',
    'activ_coef': 'Не указано'
}

defaultAim = {
    'calories': 0,
    'proteins': 0,
    'fats': 0,
    'carbs': 0
}


class Form(StatesGroup):
    name = State()
    gender = State()
    age = State()
    weight = State()
    height = State()
    avg_sleep_len = State()
    activ_coef = State()


class Dish(StatesGroup):
    category = State()
    name = State()
    proteins = State()
    fats = State()
    carbons = State()
    kcal = State()
    correct = State()
    weight = State()


food = {
    'products': {},
    'drinks': {},
    'cakes': {},
    'desserts': {},
    'sauces': {},
    'garnish': {},
    'soups': {},
    'sandwiches': {},
    'salads': {},
    'snacks': {}
}

for food_type in food.keys():
    path = os.path.join("food", str(food_type) + '.json')
    with open(path, 'r', encoding='utf-8') as file:
        food[food_type] = json.load(file)
