import asyncio
import json
import logging
import os
from pathlib import Path

import openai
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from django.shortcuts import render, redirect
import environ
from django.apps import apps
# from .models import TelegramUsers
# from usersapp.models import CustomUser
from django.contrib.auth import get_user_model
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

openai.api_key = env("GTPAPIKEY")
GPT_MODEL = "gpt-3.5-turbo"


if not os.path.exists('ai_chat_bot/users_tg_id.json'):
    with open('ai_chat_bot/users_tg_id.json', 'w') as file:
        json.dump({}, file, indent=4)


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
    info = 'This is massage from your AI Generator.'
    print(user_id)
    member = apps.get_model("usersapp.CustomUser")
    print(type(member))
    user = member.objects.get(id=11)
    print(user.first_name)
    print(fullname)
    if os.path.exists('ai_chat_bot/temp_curent_user.txt'):
        with open('ai_chat_bot/temp_curent_user.txt', 'r') as file:
            CURRENT_USER = file.read()




        with open('ai_chat_bot/users_tg_id.json', 'w') as file:
            json.dump({CURRENT_USER: user_id}, file, indent=4)


            os.remove('ai_chat_bot/temp_curent_user.txt')


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
    # print(f'******************{query}')
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{request.user.id} {request.user.first_name}')
    user = request.user

    with open('ai_chat_bot/users_tg_id.json', 'r') as file:
        telegram_user = json.load(file)
    tg_user_id = telegram_user.get(user)
    print(type(tg_user_id))
    user.telegram_id = str(tg_user_id)
    user.save()
    if tg_user_id:
        start_chatting(tg_user_id)
        return redirect(to='contactsapp:view_forms_list')
    with open('ai_chat_bot/temp_curent_user.txt', 'w') as file:
        file.write(str(CURRENT_USER))
    print(f'USER ID FROM REQUEST {CURRENT_USER}')


    return redirect(to="https://t.me/ChefHelperBot")



def start_chatting(tg_user_id):
    print('START CHATING ' + str(tg_user_id))



def generate_answer(question: str, contact):

    try:
        completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are famous comic!"},
                {"role": "user", "content": question},
            ],
            temperature=0.8,
        )
        text = completion.choices[0].message.content

    except Exception as er:
        print(er)
