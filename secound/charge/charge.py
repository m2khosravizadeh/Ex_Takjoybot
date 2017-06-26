import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .const_charge import *
from ..secound_constants import *

async def charge_func(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    my_bot_intrance = bot.getMe()
    user_id_token = str(user_id) + token
    Inline_markup4charge = InlineKeyboardMarkup(inline_keyboard=[
    [dict(text = "تایید", callback_data = "ch" + str(len(str(user_id))) + str(user_id) + 'ok' + str(len(my_bot_intrance["username"])) + my_bot_intrance["username"]),
    InlineKeyboardButton(text = "رد", callback_data = "ch" + str(len(str(user_id))) + str(user_id) + 'no' + str(len(my_bot_intrance["username"])) + my_bot_intrance["username"])]
    ])
    if Intrance == "انصراف":
        owner_stage[user_id_token] = "start_bot"
        try:
            bot.sendMessage(chat_id, Tabligh)
        except:
            pass
    elif Input_Control == "photo":
        owner_stage[user_id_token] = "start_bot"
        photo_file = bot.getFile(Intrance)
        bot_token_takjoy = telepot.Bot(token_takjoy_bot[0])
        for my_user_id in my_user_ids:
            bot_token_takjoy.sendMessage(my_user_id, bill4bot_charge.format(bot = my_bot_intrance["username"]), reply_markup = Inline_markup4charge)
            try:
                bot.sendPhoto(my_user_id, photo_file["file_id"], caption = "@" + my_bot_intrance["username"])
            except:
                bot_token_takjoy.sendMessage(my_user_id, photo_not_sent.format(bot = my_bot_intrance["username"]), reply_markup = Inline_markup4charge)




