import asyncio
import json
import os
import logging
import importlib
import utils

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from config import ADMIN_ID, BOT_TOKEN

CHAT_ID = "@collect_my_bot"
bot = Bot(token=BOT_TOKEN)
router = Router()
dispatcher = Dispatcher()
logging.basicConfig(filename='logs.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def new_user(message: types.Message):
    utils.new_user(message.from_user.id)


@router.message(Command("get_my_data"))
async def show_user_data(message: types.Message):
    text = '```\n'
    text += utils.get_user_info_as_str(message.from_user.id)
    text += '\n```'
    await message.answer(text, parse_mode='markdown')


@router.message(Command("get_my_aim"))
async def show_user_aim(message: types.Message):
    text = '```\n'
    text += 'Ваша текущая цель:\n'
    text += utils.get_user_aim_as_str(message.from_user.id)
    text += '\n```'
    await message.answer(text, parse_mode='markdown')


def add_clown(user_id):
    with open("clowns.json", "r", encoding='utf-8') as clowns:
        data = json.load(clowns)
        data[user_id] = 'is_clown'
    with open("clowns.json", "w", encoding='utf-8') as clowns:
        json.dump(data, clowns)


@router.message(Command("get_data"))
async def show_data(message: types.Message):
    add_clown(message.from_user.id)
    if not ADMIN_ID.find(str(message.from_user.id)):
        print(message.from_user.id, "is clown")
        await message.answer("🤡")
        return
    user_id = message.text[9:]
    user_id = user_id.replace(" ", "")
    await message.answer(utils.get_user_info_as_str(user_id))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


def load_routers():
    dispatcher.include_router(router)
    for file in os.listdir("commands"):
        if file.startswith("_"):
            continue
        rout = getattr(importlib.import_module(f"commands.{file[:-3]}"), "router")
        dispatcher.include_router(rout)
        logger.info(f"Router `{file}` has been loaded")


def look_req_dirs():
    if not os.path.exists("users"):
        os.mkdir("users")
    if not os.path.exists("clonws.json"):
        with open("clowns.json", "w", encoding='utf-8') as clowns:
            json.dump({}, clowns)


if __name__ == '__main__':
    look_req_dirs()
    load_routers()
    asyncio.run(main())
