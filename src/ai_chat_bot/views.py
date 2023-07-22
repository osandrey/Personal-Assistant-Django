import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from django.shortcuts import render, redirect
import environ
from django.contrib.auth import get_user_model, get_user

import django
# django.setup()
# from ..usersapp.models import CustomUser

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

"""Telegramm"""

# Bot token can be obtained via https://t.me/BotFather
TOKEN = env("TELEGRAM_BOT_TOKEN")
bot = Bot(TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
CURRENT_USER = None

def main(request):
    return render(request=request, template_name='ai_chat_bot/index.html', context={})




@dispatcher.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    language = message.from_user.locale.language
    print(language)
    hello = 'Hello'

    fullname = message.from_user.full_name
    user_id = message.from_user.id
    print(user_id)
    # User = get_user_model()

    user = CustomUser.objects.get(pk=CURRENT_USER)

    print(f'{user.username}')
    user.telegram_id = user_id
    user.save()
    info = 'This is massage from your AI Generator.'

    await message.answer(f"{hello}, <b>{fullname}!</b>\n"
                         f"{info}")


@dispatcher.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await bot.send_message()
        await message.send_copy(chat_id=message.from_user.id)
        await message.answer(text=message.text.upper())
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def on_startup(_):
    print(f'Bot started!')

def run_polling():
    try:
        # logging.basicConfig(level=logging.INFO)
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
    except Exception as error:
        print(f'Error name:{error}')


def redirect_check(request):
    global CURRENT_USER
    CURRENT_USER = request.user.id
    print(f'USER ID FROM REQUEST{CURRENT_USER}')
    return redirect(to="https://t.me/ChefHelperBot")
