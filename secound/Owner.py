import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .main import *
from .all_funcs import *
from .secound_constants import *
from .Seller.const4seller import *
from .Seller import db4seller
from .Seller.Sellers import seller_stage_func
from .setting.db_setting import db4other
from .setting.setting_constants import *
from .setting.main import setting_stage
from .db4close_store import close_store_Funnc
from .customer import customerfunc
from .post.City4Post import city4post_stage
from .account_number.account_number import account_number_func
from ..first.db_takjoy import db4takjoy
from .charge.charge import charge_func
from .charge.const_charge import *

inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [dict(text='شنبه ✅️', callback_data='شنبه'),InlineKeyboardButton(text='یکشنبه ✅', callback_data='یکشنبه')],
    [dict(text='دوشنبه ✅️', callback_data='دوشنبه'), InlineKeyboardButton(text='سه شنبه ✅️', callback_data='سه شنبه')],
    [dict(text='چهارشنبه ✅️',callback_data='چهارشنبه'), InlineKeyboardButton(text='پنجشنبه ✅', callback_data='پنجشنبه')],
    [dict(text='جمعه ✅️', callback_data='جمعه')],
    [dict(text='ثبت روز', callback_data='ثبت روز')],
    ])
    
markup4photochange = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ])

def fetch4amendment(bot, chat_id, user_id_token, message4amendment):
    try:
        ctrl_context_list.remove(user_id_token)
        owner_stage[user_id_token] = "next_ware"
        show41keys.append(user_id_token)
        bot.sendMessage(chat_id, message4amendment + "\n" + isproductokornot, reply_markup = show_result_markup)
    except:
        pass
    return

async def secound_stage(user_id, token, Intrance, Input_Control, bot, file_name, **kwargs):
    user_id_token = str(user_id) + token
    content_type = Input_Control

    if Intrance == 'درباره رباتساز 🤖':
        try:
            bot.sendMessage(user_id, Tabligh)
        except:
            pass
    else:

        if (Intrance == "خروج" or Intrance == "/start" or 
        (user_id_token in owner_stage and (owner_stage[user_id_token] in ["botsetting", "start_bot"])) and 
        content_type == "text"):
            if user_id_token in owner_stage:
                del owner_stage[user_id_token]
            if user_id_token in dic_first_button:
                del dic_first_button[user_id_token]
            if user_id_token in dic_secound_button:
                del dic_secound_button[user_id_token]
            if user_id_token in dic_context:
                del dic_context[user_id_token]
            if user_id_token in dic_title:
                del dic_title[user_id_token]
            if user_id_token in dic_currency_ware:
                del dic_currency_ware[user_id_token]
            if user_id_token in dic_unit_ware:
                del dic_unit_ware[user_id_token]
            if user_id_token in dic_price_ware:
                del dic_price_ware[user_id_token]
            if user_id_token in dic_discount:
                del dic_discount[user_id_token]
            if user_id_token in dic_photo_file:
                del dic_photo_file[user_id_token]
            if user_id_token in file_id:
                del file_id[user_id_token]
            if user_id_token in show41keys:
                show41keys.remove(user_id_token)

        if user_id_token not in owner_stage:
            owner_stage[user_id_token] = "botsetting"

        if content_type == "photo":
            if owner_stage[user_id_token] == "unit_ware":
                try:
                    my_file = Intrance
                    photo_file = bot.getFile(Intrance)
                    file_path = photo_file['file_path']
                    file_id[user_id_token] = photo_file["file_id"]
                    bot.sendMessage(user_id, give_price_ware, reply_markup=Intrance_markup)
                    owner_stage[user_id_token] = "discount"
                except:
                    pass
                if user_id_token in ctrl_context_list:
                    fetch4amendment(bot, chat_id, user_id_token)
                
            elif user_id_token in customer_stage and customer_stage[user_id_token] == "give_new_photo":
                try:
                    my_file = Intrance
                    photo_file = bot.getFile(Intrance)
                    file_path = photo_file['file_path']
                    await db4other("changeproductindb", table_name = file_name, goal = "file_id", pr = photo_file["file_id"], extitle = customer_order[user_id_token])
                    bot.sendMessage(user_id, file_id_changed, reply_markup = markup4photochange)
                    del customer_order[user_id_token]
                except:
                    pass

            elif owner_stage[user_id_token] == "charge_func":
                await charge_func(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"])
                
            else:
                try:
                    bot.sendMessage(user_id, Tabligh)
                except:
                    pass

        elif content_type == "text" or content_type == "data":        
            if content_type == "data" and Intrance[:8] == "Customer":
                await customerfunc(user_id, token, Intrance[8:], Input_Control, bot, file_name, kwargs["message_id"])
            elif owner_stage[user_id_token] == "start_bot":
                await start_bot(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"], kwargs["sellerfalg"])

            elif owner_stage[user_id_token] == "botsetting":
                await botsetting(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"], kwargs["sellerfalg"])

            elif owner_stage[user_id_token] == "first_button":
                await first_button(user_id, token, Intrance, bot)

            elif owner_stage[user_id_token] == "secound_button":
                await secound_button(user_id, token, Intrance, bot)
                
            elif owner_stage[user_id_token] == "title":
                await title(user_id, token, Intrance, bot)
                
            elif owner_stage[user_id_token] == "context":
                await context(user_id, token, Intrance, bot, file_name)
                
            elif owner_stage[user_id_token] == "photo_ware":
                await photo_ware(user_id, token, Intrance, bot)
                
            elif owner_stage[user_id_token] == "price_ware":
                await price_ware(user_id, token, Intrance, bot)
                
            elif owner_stage[user_id_token] == "currency_ware":
                await currency_ware(user_id, token, Intrance, bot)
                
            elif owner_stage[user_id_token] == "unit_ware":
                await unit_ware(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])
                
            elif owner_stage[user_id_token] == "discount":
                await discount(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])
                
            elif owner_stage[user_id_token] == "result_ware":
                await result_ware(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])
                
            elif owner_stage[user_id_token] == "amendment":
                await amendment(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])
                
            elif owner_stage[user_id_token] == "next_ware":
                await next_ware(user_id, token, Intrance, bot, file_name)

            elif owner_stage[user_id_token] == "day_showing":
                await day_showing(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])

            elif owner_stage[user_id_token] == "closed_store":
                await closed_store(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])

            elif owner_stage[user_id_token] == "opened_store":
                await opened_store(user_id, token, Intrance, bot, file_name, Input_Control, kwargs["message_id"])

            elif owner_stage[user_id_token] == "setting_stage":
                await setting_stage(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"])
            
            elif owner_stage[user_id_token] == "seller_stage" and not kwargs["sellerfalg"]:
                await seller_stage_func(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"])

            elif owner_stage[user_id_token] == "city4post_stage":
                await city4post_stage(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"])            
                
            elif owner_stage[user_id_token] == "account_number_stage":
                await account_number_func(user_id, token, Intrance, Input_Control, bot, file_name, kwargs["message_id"])
        else:
            try:
                bot.sendMessage(user_id, "لطفا اطلاعات خواسته شده را درست وارد کنید.")    
            except:
                pass

async def start_bot(chat_id, token, Intrance, Input_Control, bot, file_name, message_id, sellerflag):
    try:
        user_id_token = str(chat_id) + token
        bot.sendMessage(chat_id, Tabligh)
        await botsetting(chat_id, token, Intrance, Input_Control, bot, file_name, message_id, sellerflag)  
    except:
        pass
async def botsetting(chat_id, token, Intrance, Input_Control, bot, file_name, message_id, sellerflag):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_botsetting(Intrance, bot, chat_id, token)
    
    if user_id_token in shown4customer:
        del shown4customer[user_id_token]
    if not flag_Intrance:
        if Intrance == 'تنظیمات ⚙':
            owner_stage[user_id_token] = "setting_stage"
            await setting_stage(chat_id, token, Intrance, Input_Control, bot, file_name, message_id)
            user_in_setting.append(user_id_token)

        elif Intrance == 'شماره حساب':
            try:
                owner_stage[user_id_token] = "account_number_stage"
                bot.sendMessage(chat_id, choose_account_setting, reply_markup = account_markup)
            except:
                pass
                        
        elif Intrance == 'باز کردن 🔓' and token in close_store:
            try:
                close_store.remove(token)
                await close_store_Funnc(1 , Store_Specifications = token)
                bot.sendMessage(chat_id, store_is_open, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))           
            except:
                pass
        elif Intrance == 'تعطیل 🔒' and token not in close_store:
            try:                    
                close_store.append(token)
                await close_store_Funnc(0 , Store_Specifications = token)
                bot.sendMessage(chat_id, store_is_closed, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
            except:
                pass

        elif not sellerflag:
            if Intrance == 'فروشندگان 👥':
                try:
                    sellers = seller_dict[user_id_token]
                    show_sellers = "لیست یوزرنیم فروشندگان: \n"

                    if sellers:
                        seller_keys = markup4seller
                        for seller in sellers:
                            if seller[1] != None:
                                show_sellers += "@" + seller[1] + "\n"

                    else:
                        seller_keys = markup4noseller
                        show_sellers = "فروشنده‌ای معرفی نشده است. \n لطفا فروشنده معرفی نمایید."
                    bot.sendMessage(chat_id, show_sellers, reply_markup = seller_keys)
                    owner_stage[user_id_token] = "seller_stage"
                except:
                    pass
            elif Intrance ==  'پست 📬':
                try:
                    bot.sendMessage(chat_id, createoreditcity4post, reply_markup = AEcitypostkeys)
                    owner_stage[user_id_token] = "city4post_stage"
                except:
                    pass
            elif Intrance == 'شارژ ربات ⛽️':
                try:
                    temp_message =""
                    for charge_details in list4charge:
                        temp_message += message4charge.format(acc_num = charge_details[0], name = charge_details[2], acc_bank = charge_details[1])
                    bot.sendMessage(chat_id, pay_price.format(price = "۲۰,۰۰۰") + temp_message, reply_markup = markup_give_title)
                    owner_stage[user_id_token] = "charge_func"
                except:
                    pass
                
            else:
                if token in close_store:
                    try:
                        bot.sendMessage(chat_id, Start_New_Bot, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
                    except:
                        pass
                else:
                    try:
                        bot.sendMessage(chat_id, Start_New_Bot, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))
                    except:
                        pass

        else:
            if token in close_store:
                try:
                    bot.sendMessage(chat_id, Start_New_Bot, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
                except:
                    pass
            else:
                try:
                    bot.sendMessage(chat_id, Start_New_Bot, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))
                except:
                    pass

async def first_button(chat_id, token, Intrance, bot):
    user_id_token = str(chat_id) + token
    flag_Intrance=test_Intrance_first_button(Intrance, bot, chat_id , token)      
    
    if flag_Intrance == 'back':
        owner_stage[user_id_token] = "start_bot"
        
    elif flag_Intrance == 'closed_store':
        owner_stage[user_id_token] = "closed_store"

    elif flag_Intrance == 'opened_store':
        owner_stage[user_id_token] = "opened_store"
        
    elif flag_Intrance == 'next':

        owner_stage[user_id_token] = "secound_button"
        
    elif flag_Intrance == "None":
        try:
            bot.sendMessage(chat_id, Tabligh, reply_markup = bot_setting_markup)
        except:
            pass
            
async def secound_button(chat_id, token, Intrance, bot):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_secound_button(Intrance, bot, chat_id, token)
    
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == 'context':
        owner_stage[user_id_token] = "context"

    elif flag_Intrance == "None":
        try:
            dic_first_button[user_id_token]= Intrance
            owner_stage[user_id_token] = "title"
            bot.sendMessage(chat_id, result1 + Intrance + result2, reply_markup = Intrance_markup)
        except:
            pass

async def title(chat_id, token, Intrance, bot):
    
    user_id_token = str(chat_id) + token
    flag_Intrance=test_Intrance_title(Intrance, bot, chat_id, token)
    
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == 'context':
        owner_stage[user_id_token] = "context"

        
    elif flag_Intrance == "None":
        try:
            owner_stage[user_id_token] = "context"
            dic_secound_button[user_id_token]= Intrance        
            result = dic_first_button[user_id_token] + "/" + Intrance + "\n"         
            bot.sendMessage(chat_id, result12 + result + give_title, reply_markup = markup_give_title)
        except:
            pass
async def context(chat_id, token, Intrance, bot, file_name, **kw_context_arg):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_context(Intrance, bot, chat_id, token)    

    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == "None":
        try:
            titlesfromdb = await close_store_Funnc("check_title_repetitive" , column = "title", table_name = file_name)
            if Intrance not in titlesfromdb:
                owner_stage[user_id_token] = "photo_ware"
                dic_title[user_id_token]= Intrance
                if user_id_token in ctrl_context_list:
                    fetch4amendment(bot, chat_id, user_id_token, title_changed)
                else:
                    bot.sendMessage(chat_id, give_context, reply_markup = Intrance_markup)
            else:
                bot.sendMessage(chat_id, title_repetetive, reply_markup = Intrance_markup)
        except:
            pass
async def photo_ware(chat_id, token, Intrance, bot):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_photo_ware(Intrance, bot, chat_id, token)
    
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == 'unit_ware':
        if user_id_token in dic_context:
            dic_context[user_id_token] = None
        owner_stage[user_id_token] = "unit_ware"
        if user_id_token in ctrl_context_list:
            fetch4amendment(bot, chat_id, user_id_token, context_not_exists)
        else:
            try:
                bot.sendMessage(chat_id, give_photo_ware)
            except:
                pass

    elif flag_Intrance == "None":
        try:
            dic_context[user_id_token]= Intrance
            owner_stage[user_id_token] = "unit_ware"
            if user_id_token in ctrl_context_list:
                fetch4amendment(bot, chat_id, user_id_token, context_changed)
            else:
                bot.sendMessage(chat_id, give_photo_ware)
        except:
            pass

async def unit_ware(chat_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(chat_id) + token
    flag_Intrance=test_Intrance_unit_ware(Intrance, bot, chat_id, token)

    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"
    elif flag_Intrance == "discount":
        owner_stage[user_id_token] = "discount"
        if user_id_token in file_id:
            file_id[user_id_token] = None
        if user_id_token in ctrl_context_list:
            fetch4amendment(bot, chat_id, user_id_token, phexist_cancelled)
        else:
            try:
                bot.sendMessage(chat_id, give_price_ware, reply_markup=Intrance_markup)
            except:
                pass
    elif flag_Intrance == "None":
        try:
            bot.sendMessage(chat_id, Tabligh)
            bot.sendMessage(chat_id, give_photo_ware)
        except:
            pass

async def price_ware(chat_id, token, Intrance, bot):
    user_id_token = str(chat_id) + token

    flag_Intrance=test_Intrance_price_ware(Intrance, bot, chat_id, token)
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == "None":
        try:
            owner_stage[user_id_token] = "discount"
            bot.sendMessage(chat_id, give_price_ware, reply_markup = Intrance_markup)
            dic_unit_ware[user_id_token]= Intrance
        except:
            pass

async def currency_ware(chat_id, token, Intrance, bot):
    user_id_token = str(chat_id) + token
    flag_Intrance=test_Intrance_currency_ware(Intrance, bot, chat_id, token)
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == "None":
        if Intrance.isdigit():
            if int(Intrance) > 10000000000:
                try:
                    bot.sendMessage(chat_id, Error_price)
                except:
                    pass
            else:
                try:
                    dic_price_ware[user_id_token]= Intrance
                    bot.sendMessage(chat_id, give_discount, reply_markup=discount_markup)
                    owner_stage[user_id_token] = "result_ware"
                except:
                    pass
        else:
            try:
                bot.sendMessage(chat_id, mistake_price_ware, reply_markup=markup_give_title)
            except:
                pass
            
     
async def discount(chat_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_discount(Intrance, bot, chat_id, token)
    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == "None":
        if Intrance.isdigit():
            if int(Intrance) > 10000000000:
                try:
                    bot.sendMessage(chat_id, Error_price)
                except:
                    pass
            else:
                owner_stage[user_id_token] = "result_ware"
                dic_currency_ware[user_id_token] = "تومان"
                dic_price_ware[user_id_token] = Intrance
                if user_id_token in ctrl_context_list:
                    fetch4amendment(bot, chat_id, user_id_token, price_changed)
                else:
                    try:
                        bot.sendMessage(chat_id, give_discount, reply_markup = discount_markup)
                    except:
                        pass
        else:
            try:
                bot.sendMessage(chat_id, mistake_price_ware, reply_markup = markup_give_title)
            except:
                pass

    elif flag_Intrance == 'result_ware':
        if user_id_token in ctrl_context_list:
            dic_discount[user_id_token] = None
            dic_price_ware[user_id_token] = None
            fetch4amendment(bot, chat_id, user_id_token, no_price_existed)
            
        else:
            await day_showing(chat_id, token, Intrance, bot, file_name, Input_Control, message_id)
            dic_price_ware[user_id_token] = None


async def result_ware(chat_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(chat_id) + token
    flag_Intrance=test_Intrance_result_ware(Intrance, bot, chat_id, token)

    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == 'day_showing':
        owner_stage[user_id_token] = "day_showing"
        show_result_ware(Intrance, bot, chat_id, user_id_token)
        if user_id_token in ctrl_context_list:
            if user_id_token in dic_discount:
                del dic_discount[user_id_token]
            fetch4amendment(bot, chat_id, user_id_token, gndiscount_cancelled)
        else:
            await day_showing(chat_id, token, Intrance, bot, file_name, Input_Control, message_id)
    elif flag_Intrance == "None":
        if Intrance.isdigit():
            discountـtemp = int(Intrance)
            if discountـtemp >= 100 or discountـtemp < 0:
                try:
                    bot.sendMessage(chat_id, mistake_discount, reply_markup = markup_give_title)
                except:
                    pass
            else:
                dic_discount[user_id_token]= Intrance
                owner_stage[user_id_token] = "day_showing"
                show_result_ware(Intrance, bot, chat_id, user_id_token)
                if user_id_token in ctrl_context_list:
                    fetch4amendment(bot, chat_id, user_id_token, discount_changed)
                else:
                    await day_showing(chat_id, token, Intrance, bot, file_name, Input_Control, message_id)    
        else:
            try:
                bot.sendMessage(chat_id, mistake_discount, reply_markup = markup_give_title)
            except:
                pass

async def day_showing(chat_id, token, Intrance, bot, file_name, Input_Control, message_id):

    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_day_showing(Intrance, bot, chat_id, token)
    if flag_Intrance != "None":
        owner_stage[user_id_token] = "start_bot"
    if user_id_token in show41keys:
        msg_change = True
        if Input_Control == "data":
            if Intrance in showindays[user_id_token]:
                showindays[user_id_token].remove(Intrance)
            elif Intrance == "ثبت روز":
                owner_stage[user_id_token] = "next_ware"
                shown_days = ""
                i_counter = 1
                day_code[user_id_token] = 0
                for shown_day in showindays[user_id_token]:
                    day_code[user_id_token] += day4code[shown_day]
                    shown_days += shown_day
                    if i_counter < len(showindays[user_id_token]):
                        shown_days += " - "
                        i_counter += 1
                try:
                    bot.editMessageText(message_id, give_day_setting + "\n" + shown_days)
                    bot.sendMessage(chat_id, isproductokornot, reply_markup = show_result_markup)
                    show41keys.remove(user_id_token)
                    msg_change = False
                except:
                    pass
            else:
                showindays[user_id_token].append(Intrance)

            if msg_change:
                try:
                    str_inline_buttons = await making_inline_buttons(*showindays[user_id_token])
                    inline_buttons = InlineKeyboardMarkup(inline_keyboard = str_inline_buttons)           
                    bot.editMessageText(message_id, give_day_setting, reply_markup = inline_buttons)           
                except:
                    pass
        elif Input_Control == "message":
            flag_Intrance = test_Intrance_day_showing(Intrance, bot, chat_id)
            
            if flag_Intrance == "back_start":
                owner_stage[user_id_token] = "start_bot"

            elif flag_Intrance == "next_ware":
                shown_days = ""
                i_counter = 1
                for shown_day in showindays[user_id_token]:
                    shown_days += shown_day
                    if i_counter < len(showindays[user_id_token]):
                        shown_days += " - "
                        i_counter += 1
                try:
                    bot.editMessageText(message_id, give_day_setting + "\n" + shown_days, reply_markup = markup)
                    show41keys.remove(user_id_token)
                    await next_ware(chat_id, token, Intrance, bot, file_name)
                except:
                    pass
    else:
        owner_stage[user_id_token] = "day_showing"
        show41keys.append(user_id_token)
        showindays[user_id_token] = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        try:
            bot.sendMessage(chat_id, daysetting4what, reply_markup = markup_give_title)
            bot.sendMessage(chat_id, give_day_setting, reply_markup = inline_markup)
        except:
            pass

async def next_ware(chat_id, token, Intrance, bot, file_name):
    user_id_token = str(chat_id) + token
    flag_Intrance = test_Intrance_next_ware(Intrance, bot, chat_id, token)

    if flag_Intrance == 'back_start':
        owner_stage[user_id_token] = "start_bot"
        
    elif flag_Intrance == 'amendment':
        try:
            if user_id_token in dic_price_ware and dic_price_ware[user_id_token]:
                bot.sendMessage(chat_id, witch_portion_edit, reply_markup = markup4edition)
            else:
                bot.sendMessage(chat_id, witch_portion_edit, reply_markup = markupnot4edition)
            owner_stage[user_id_token] = "amendment"
        except:
            pass
    elif flag_Intrance == 'next_ware':
        if user_id_token in ctrl_context_list:
            ctrl_context_list.remove(user_id_token)
        await db4takjoy(3, chat_id = chat_id, table_name = file_name, key_acc = user_id_token)
        owner_stage[user_id_token] = "botsetting"
        try:
            bot.sendMessage(chat_id, saved_in_db)
            if token in close_store:
                bot.sendMessage(chat_id, give_next_ware, reply_markup=store_markup("باز کردن 🔓", user_id_token = user_id_token))
            else:
                bot.sendMessage(chat_id, give_next_ware, reply_markup=store_markup("تعطیل 🔒", user_id_token = user_id_token))
        except:
            pass
async def amendment(user_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(user_id) + token
    if user_id_token in show41keys:
        show41keys.remove(user_id_token)
    if Intrance == "موضوع":
        try:
            bot.sendMessage(user_id, give_title, reply_markup = markup_give_title)
            owner_stage[user_id_token] = "context"
            ctrl_context_list.append(user_id_token)
        except:
            pass
    elif Intrance == 'متن محصول':
        try:
            bot.sendMessage(user_id, give_context, reply_markup = Intrance_markup)
            owner_stage[user_id_token] = "photo_ware"
            ctrl_context_list.append(user_id_token)
        except:
            pass

    elif Intrance == 'عکس محصول':
        try:
            bot.sendMessage(user_id, give_photo_ware, reply_markup = Intrance_markup)
            owner_stage[user_id_token] = "unit_ware"
            ctrl_context_list.append(user_id_token)
        except:
            pass
    elif Intrance == 'روزهای نمایش':
        owner_stage[user_id_token] = "day_showing"
        ctrl_context_list.append(user_id_token)
        await day_showing(user_id, token, Intrance, bot, file_name, Input_Control, message_id)
    elif Intrance == 'قیمت':
        try:
            owner_stage[user_id_token] = "discount"
            ctrl_context_list.append(user_id_token)
            bot.sendMessage(user_id, give_price_ware, reply_markup = Intrance_markup)
        except:
            pass
    elif Intrance == 'تخفیف' and user_id_token in dic_price_ware:
        try:
            owner_stage[user_id_token] = "result_ware"
            ctrl_context_list.append(user_id_token)
            bot.sendMessage(user_id, give_discount, reply_markup = discount_markup)
        except:
            pass
    elif Intrance == 'انصراف':
        owner_stage[user_id_token] = "next_ware"
        await next_ware(chat_id, token, Intrance, bot, file_name)

async def closed_store(user_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(user_id) + token
    flag_Intrance=test_Intrance_closed_store(Intrance, bot, user_id)        

    if flag_Intrance == 'back':
        owner_stage[user_id_token] = "start_bot"

    elif flag_Intrance == 'open_store':
        close_store.remove(token)
        await close_store_Funnc(1 , Store_Specifications = token)
        owner_stage[user_id_token] = "opened_store"
        
    elif flag_Intrance == 'Products':
        owner_stage[user_id_token] = "secound_button"
        
    elif flag_Intrance == "None":
        try:
            bot.sendMessage(chat_id, Tabligh)
        except:
            pass

async def opened_store(user_id, token, Intrance, bot, file_name, Input_Control, message_id):
    user_id_token = str(user_id) + token
    flag_Intrance=test_Intrance_opened_store(Intrance, bot, user_id)        

    if flag_Intrance == 'back':
        owner_stage[user_id_token] = "start_bot"
        
    elif flag_Intrance == 'close_store':
        close_store.append(token)
        await close_store_Funnc(0 , Store_Specifications = token)
        owner_stage[user_id_token] = "closed_store"

    elif flag_Intrance == 'Products':
        owner_stage[user_id_token] = "secound_button"
        
    elif flag_Intrance == "None":
        try:
            bot.sendMessage(chat_id, Tabligh)
        except:
            pass

