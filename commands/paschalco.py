from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("rub_500"))
async def rub_500(message: types.Message):
    await message.answer_animation(types.FSInputFile("twerk.gif"))


@router.message(Command("help"))
async def _help(message: types.Message):
    await message.answer("/help - все команды"
                         "\n/start - Добавить себя в базу данных"
                         "\n/rub_500 - <a href = \"https://www.youtube.com/watch?v=g7jPuEpjvdA\">тверк от жениха</a>",
                         parse_mode='HTML')
