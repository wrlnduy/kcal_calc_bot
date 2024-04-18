from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from utils import set_keyboard
from config import Dish

router = Router()


@router.message(Command("add_food"))
async def new_food(message: types.Message, state: FSMContext):
    await state.set_state(Dish.category)
    await message.answer(
        "К какой из категорий ниже Вы бы отнесли своё блюдо?",
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
        )
    )


@router.callback_query(Dish.category)
async def choose_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(category=call.data)
    await state.set_state(Dish.name)
    await call.message.answer(
        "Название блюда / продукта:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Dish.name)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.proteins)
    await message.answer(
        "Белки, г:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Dish.proteins)
async def add_proteins(message: types.Message, state: FSMContext):
    await state.update_data(proteins=message.text)
    await state.set_state(Dish.fats)
    await message.answer(
        "Жиры, г:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Dish.fats)
async def add_fats(message: types.Message, state: FSMContext):
    await state.update_data(fats=message.text)
    await state.set_state(Dish.carbons)
    await message.answer(
        "Углеводы, г:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Dish.carbons)
async def add_carbons(message: types.Message, state: FSMContext):
    await state.update_data(carbons=message.text)
    await state.set_state(Dish.kcal)
    await message.answer(
        "Калории, ккал:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Dish.kcal)
async def add_kcal(message: types.Message, state: FSMContext):
    await state.set_state(Dish.correct)
    dish = await state.update_data(kcal=message.text)
    info = dish['name']
    info += "\nБелки, г: " + dish['proteins']
    info += "\nЖиры, г: " + dish['fats']
    info += "\nУглеводы, г: " + dish['carbons']
    info += "\nКалории, ккал: " + dish['kcal']
    info += "\nВсё верно?"
    await message.answer(
        info,
        reply_markup=set_keyboard(
            {
                'Да': '1',
                'Нет': '0'
            }
        )
    )


@router.callback_query(Dish.correct)
async def result(call: CallbackQuery):
    if call.data == '1':
        await call.message.answer("Теперь Вы сможете найти своё блюдо в списках. \nИспользуйте команду '/find_food'")
        # new_new_dish()
    else:
        await call.message.answer("Будьте внимательны и попробуйте ещё раз. \nИспользуйте команду '/add_food' снова")
