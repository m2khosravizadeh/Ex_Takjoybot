import asyncio
import telepot
import telepot.aio
import datetime

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from . import MessageTexts
from .new_token import token_change
from .bot_username import check_username_token
from .Bugs import Test_Token, is_int
from .db_takjoy import db4takjoy
from ..secound.secound_constants import *

markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='تغییر توکن')],
    ])

change_token_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='بازگشت')],
    ])

async def test_Intrance(Intrance, bot, chat_id, markup):

    if Intrance == '/start':
        try:
            await bot.sendMessage(chat_id, MessageTexts.takjoy_presentation, reply_markup=markup)
            await bot.sendMessage(chat_id, MessageTexts.robot_presentation, reply_markup=markup)
            return True
        except:
            pass

    elif Intrance == '/revoke':
        try:
            await bot.sendMessage(chat_id, MessageTexts.robot_presentation2, reply_markup=markup)        
            return True
        except:
            pass
    else:
        return False
    
async def Intrance4handle(Intrance, chat_id, markup, **fargs):
    bot = fargs["_bot"]
    tool_matn = len(Intrance)
    flag_Intrance = await test_Intrance(Intrance, bot, chat_id, markup)        

    if not flag_Intrance:
        if Intrance == 'تغییر توکن':
            usernames= await check_username_token(chat_id)

            if not usernames:
                try:
                    await bot.sendMessage(chat_id, MessageTexts.notocken4u, reply_markup = change_token_markup)    
                    MessageTexts.give_token = 1
                except:
                    pass
            elif len(usernames) == 1:
                try:
                    await bot.sendMessage(chat_id, MessageTexts.insert_changed_Token, reply_markup = change_token_markup)
                    MessageTexts.give_token = 3
                except:
                    pass
            else:
                global token_change_markup
                try:
                    token_change_markup = await token_change(usernames)
                    await bot.sendMessage(chat_id, MessageTexts.select_your_bot, reply_markup = token_change_markup)
                except:
                    pass
        else:
            await Token_Typos(bot, tool_matn, Intrance, chat_id, markup, 1, **fargs)


async def Token_Typos(bot, tool_matn, Intrance, chat_id, change_token_markup, db_control, **fargs):
    if (((tool_matn > 40) and (tool_matn < 50)) and ((Intrance[8:9] == ":") or (Intrance[9:10] == ":") or (Intrance[10:11] == ":")) and is_int(Intrance[:8])):
        if ((tool_matn == 45) and (Intrance[9:10] == ":") and (is_int(Intrance[:9]))):
            test_token = Test_Token(Intrance, chat_id)
            my_bot_intrance = None
            try:
                bot_intrance = telepot.Bot(Intrance)
                my_bot_intrance = bot_intrance.getMe()
            except:
                await bot.sendMessage(chat_id, MessageTexts.Token_not_accepted, reply_markup = markup)
            if my_bot_intrance and my_bot_intrance["username"] not in list_bot_id:
                await bot.sendMessage(chat_id, MessageTexts.tnx4takjoy_use.format(bot = "@" + my_bot_intrance["username"]), reply_markup=markup)
            else:
                await bot.sendMessage(chat_id, MessageTexts.Token_repeated, reply_markup=markup)
                my_bot_intrance = None
            if my_bot_intrance:
                for my_user_id in my_user_ids:
                    try:
                        await bot.sendMessage(my_user_id, MessageTexts.dude_make_bot.format(u_name = fargs["username"], u_id = str(chat_id), bot = "@" + my_bot_intrance["username"]))
                    except:
                        pass
                MessageTexts.true_token[chat_id] = Intrance
                MessageTexts.saveindb.append(chat_id)
                await db4takjoy(0, Bot_id = my_bot_intrance["username"], Daysetting = 7)
                Date_bot[my_bot_intrance["username"]] = datetime.date.today() + datetime.timedelta(days=7)
                await db4takjoy(1)


    else:
        try:
            await bot.sendMessage(chat_id, MessageTexts.Tabligh, reply_markup=markup)
        except:
            pass
