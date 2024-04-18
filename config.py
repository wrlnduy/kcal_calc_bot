import os

from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

defaultForm = {
    'name': 'Не указано',
    'gender': 'Не указано',
    'age': 'Не указано',
    'weight': 'Не указано',
    'height': 'Не указано',
    'avg_sleep_len': 'Не указано',
    'activity_coefficient': 'Не указано'
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
