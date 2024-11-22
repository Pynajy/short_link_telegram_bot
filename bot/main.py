import subprocess
import asyncio
import logging
import sys
import os
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand

from aiogram.fsm.context import FSMContext

from data.api.main import (
    check_user,
    add_link,
    list_link,
)

from data.tools.is_url import is_url

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await check_user(message.from_user.id)
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\nЯ бот для сокращения ссылок, отправь мне ссылку и я дам тебе её короткий вариант")


@dp.message(F.text == "/listlink")
async def send_welcome(message: Message, state: FSMContext) -> None:
    list_links = await list_link(message.from_user.id)
    if list_links["status"]:
        msg = ""
        for link in list_links["short_links"]:
            msg += f"Короткая ссылка: af-link.ru/{link['code']}\nОригинальная ссылка: {link['link']}\n\n"

        await message.answer(msg)
    else:
        await message.answer("У нас какие то проблемы, но мы их уже решаем") 


@dp.message()
async def create_short_link(message: Message) -> None:
    if await is_url(message.text):
        short_link = await add_link(message.from_user.id, message.text)
        if short_link["status"]:
            await message.answer(short_link["link"])
        else:
            await message.answer("У нас какие то проблемы, но мы их уже решаем")
    else:
        await message.answer("Данный текст не похож на ссылку, возможно вы где то допустили ошибку")


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="addlink", description="Сократить ссылку"),
        BotCommand(command="listlink", description="Мои ссылки"),
        BotCommand(command="deletelink", description="Удалить ссылку"),
    ])


async def main() -> None:
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())