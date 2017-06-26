import time
import string
import asyncio
import telepot
import telepot.aio

from concurrent.futures import ProcessPoolExecutor
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import timedelta, datetime

from . import MessageTexts
from .db_takjoy import db4takjoy
from . import bot_username
from .Bugs import Test_Token, is_int
from .handle import Intrance4handle, test_Intrance
from ..secound.charge.const_charge import *
from ..secound.secound_constants import *
from ..secound.Seller.const4seller import *
from ..secound.Seller.constdb4dbseller import *

global choose_file, Bot

markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='تغییر توکن')],
    ], resize_keyboard = True)

change_token_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='بازگشت')],
    ], resize_keyboard = True)
    
markup4change_token = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='انصراف')],
    ], resize_keyboard = True)

def func_Inline_markup(*bot_ids):
    list4bot_id = []
    for bot_id in bot_ids:
        if bot_id != None:        
            list4bot_id.append([dict(text = "@" + bot_id, callback_data = "ct" + bot_id)])
    list4bot_id.append([dict(text = 'انصراف', callback_data = "ct_cancelled")])
    return list4bot_id
    
async def start_control(chat_id, Intrance, content_type, **fargs):
    bot = fargs["_bot"]
    if chat_id not in MessageTexts.give_token:
        MessageTexts.give_token[chat_id] = 1
    
    if content_type == 'text':
        if Intrance == 'راهنمایی':
            try:
                await bot.sendMessage(chat_id, MessageTexts.robot_presentation + MessageTexts.robot_presentation2 + MessageTexts.robot_presentation3, reply_markup=markup)        
            except:
                pass
        elif Intrance == 'پشتیبانی':
            try:
                await bot.sendMessage(chat_id, MessageTexts.Guidance, reply_markup = markup)
            except:
                pass

        elif Intrance == "تغییر توکن":
            if str(chat_id) not in dict4bot_ids4users:
                try:
                    await bot.sendMessage(chat_id, no_bot)
                except:
                    pass
            else:
                try:
                    Inline_markup4bot_ids = func_Inline_markup(*dict4bot_ids4users[str(chat_id)])
                    await bot.sendMessage(chat_id, witch_bot, reply_markup = InlineKeyboardMarkup(inline_keyboard = Inline_markup4bot_ids))
                except:
                    pass
        elif MessageTexts.give_token[chat_id] == 1:
            await handle(chat_id, Intrance, **fargs)

        elif MessageTexts.give_token[chat_id] == 3:
            await change_token(chat_id, Intrance)
            
        elif MessageTexts.give_token[chat_id] == "token4change":
            if Intrance == 'انصراف':
                try:
                    await bot.sendMessage(chat_id, MessageTexts.Tokens_not_changed, reply_markup = markup)
                    del MessageTexts.give_token[chat_id]
                except:
                    pass
            else:
                try:
                    temp_bot = telepot.aio.Bot(Intrance)
                    my_bot_intrance = await temp_bot.getMe()
                except:
                    my_bot_intrance = None
                if my_bot_intrance and my_bot_intrance["username"] == MessageTexts.save_token[chat_id]:
                    del MessageTexts.give_token[chat_id]
                    await db4takjoy("chang_token", new_token = Intrance, bot_id = my_bot_intrance["username"])
                    try:
                        await bot.sendMessage(chat_id, MessageTexts.Token_changed.format(bot = my_bot_intrance["username"]))
                        ex_token = dic4charge_bot_id2token[my_bot_intrance["username"]]
                        dic4charge_bot_id2token[my_bot_intrance["username"]] = Intrance
                        e_num = dict_token2e_num[ex_token]
                        del dict_token2e_num[ex_token]
                        dict_token2e_num[Intrance] = e_num
                        UNT_Dict[e_num][1] = Intrance
                        del user_id4owner[ex_token]
                        user_id_owner = str(chat_id) + Intrance
                        user_id4owner[Intrance] = user_id_owner
                        ex_use_id_owner = str(chat_id) + ex_token
                        temp_seller_dict = seller_dict[ex_use_id_owner]
                        seller_dict[user_id_owner] = temp_seller_dict
                        print("dic_user_id[e_num] is: ", dic_user_id[e_num])
                        if e_num in dic_user_id:
                            for u_id_customer in dic_user_id[e_num]:
                                for i in range(0, len(list4customer_chars) - 1):
                                    if u_id_customer != "None":
                                        my_temp = list4customer_chars[i][str(u_id_customer) + ex_token]
                                        del list4customer_chars[i][str(u_id_customer) + ex_token]
                                        list4customer_chars[i][str(u_id_customer) + Intrance] = my_temp
                    except:
                        pass
                else:
                    try:
                        await bot.sendMessage(chat_id, MessageTexts.Token_is_not_correct)
                    except:
                        pass

async def handle(chat_id, Intrance, **fargs):
    MessageTexts.flag_test_un[chat_id] = 1
    
    tool_matn = len(Intrance)
    markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='تغییر توکن')],
    ], resize_keyboard = True)
    change_token_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی'), KeyboardButton(text='تغییر توکن')],
    ], resize_keyboard = True)
    
    await Intrance4handle(Intrance, chat_id, markup, **fargs)

async def on_callback_query(user_id, msg_idf, bot, data, **Cwargs):
    if data[:2] == "ch":
        u_id_count = int(data[2:3])
        callback4okacc = data[:u_id_count + 3] + 'oa' + data[u_id_count + 5:]
        callback4noacc = data[:u_id_count + 3] + 'na' + data[u_id_count + 5:]
        callback4okrefused = data[:u_id_count + 3] + 'or' + data[u_id_count + 5:]
        callback4norefused = data[:u_id_count + 3] + 'nr' + data[u_id_count + 5:]
        Inline_markup4charge = InlineKeyboardMarkup(inline_keyboard=[
                                [dict(text = "تایید", callback_data = data[:u_id_count + 3] + 'ok' + data[u_id_count + 5:]),
                                InlineKeyboardButton(text = "رد", callback_data = data[:u_id_count + 3] + 'no' + data[u_id_count + 5:])]])
        Inline_markup4chargeok =  InlineKeyboardMarkup(inline_keyboard=[
                                 [dict(text = "بله", callback_data = callback4okacc),
                                 InlineKeyboardButton(text = "خیر", callback_data = callback4okrefused)]
                                 ])
        Inline_markup4chargeno = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text = "بله", callback_data = callback4noacc),
            InlineKeyboardButton(text = "خیر", callback_data = callback4norefused)]
        ])

        if user_id in my_user_ids:
            data = data[3:]

            if data[u_id_count:u_id_count + 2] == "ok":
                try:
                    await bot.editMessageText(msg_idf, MessageTexts.are_u_sure_ok, reply_markup = Inline_markup4chargeok)
                except:
                    pass
            elif data[u_id_count:u_id_count + 2] == "no":
                try:
                    await bot.editMessageText(msg_idf, MessageTexts.are_u_sure_no, reply_markup = Inline_markup4chargeno)
                except:
                    pass
            elif data[u_id_count:u_id_count + 2] == "oa":
                print("in oa: ", data[u_id_count + 4:])
                await db4takjoy("charge_bot", bot_id = data[u_id_count + 4:], day = "30")
                Date_bot[data[u_id_count + 4:]] += timedelta(days = 30)
                print("Date_bot[data[u_id_count+3:]] :", Date_bot[data[u_id_count+4:]])
                await bot.editMessageText(msg_idf, MessageTexts.thirth_days_adding.format(day = str((Date_bot[data[u_id_count+4:]] - datetime.now()).days)))
                for u_id in my_user_ids:
                    await bot.sendMessage(u_id, MessageTexts.thirth_days_adding.format(day = str((Date_bot[data[u_id_count+4:]] - datetime.now()).days)))
            elif data[u_id_count:u_id_count+2] == "or" or data[u_id_count:u_id_count+2] == "nr":
                try:
                    await bot.editMessageText(msg_idf, MessageTexts.bill4bot_charge.format(bot = data[u_id_count+4:]), reply_markup = Inline_markup4charge)
                except:
                    pass
            elif data[u_id_count:u_id_count + 2] == "na":
                bot_takjoy = telepot.aio.Bot(dic4charge_bot_id2token[data[u_id_count + 2:]])
                try:
                    await bot_takjoy.sendMessage(data[:u_id_count], billnotaccepted)
                    await bot.editMessageText(msg_idf, billrefusion.format(bot = data[u_id_count + 4:]))
                except:
                    pass
    elif data[:2] == "ct":
        data = data[2:]
        if data == "_cancelled":
            try:
                await bot.editMessageText(msg_idf, MessageTexts.Tokens_not_changed)
            except:
                pass
        else:
            try:
                await bot.editMessageText(msg_idf, MessageTexts.token_changing.format(bot = data))
                await bot.sendMessage(user_id, MessageTexts.insert_changed_Token, reply_markup = markup4change_token)
                MessageTexts.give_token[user_id] = "token4change"
                MessageTexts.save_token[user_id] = data
            except:
                pass
async def change_token(chat_id, Intrance):
    tool_matn = len(Intrance)
    flag_chek_Token = await test_Intrance(Intrance, bot, chat_id, markup)        
    if not flag_chek_Token:
        if Intrance == "بازگشت":
            try:
                MessageTexts.give_token = 1
                await bot.sendMessage(chat_id, MessageTexts.cancelled_change_token, reply_markup = change_token_markup)
            except:
                pass
        else:
            temp_token = [Intrance ,MessageTexts.impermanent_token[chat_id]]
            MessageTexts.save_new_token[chat_id] = temp_token
            try:
                await bot.sendMessage(chat_id, MessageTexts.OK_change_token, reply_markup=change_token_markup)
                MessageTexts.changeindb.append[chat_id]
                await db4takjoy(2)
            except:
                pass
async def secound_def():
    while True:
        first_token()
        if MessageTexts.saveindb:        
            await db4takjoy(0, Daysetting = "7")
        if MessageTexts.changeindb:
            await db4takjoy(2)

def first_token():    
    MessageTexts.loop = asyncio.get_event_loop()
    bot = telepot.aio.Bot(MessageTexts.Bot_Token[0])
    loop.create_task(bot.message_loop({'chat':start_control,
                                       'callback_query':on_callback_query}))
    loop.run_forever()
   
