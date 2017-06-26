import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .const4seller import *
from .db4seller import *
from ..all_funcs import *
from ..secound_constants import *

markup4chseller = ReplyKeyboardMarkup(keyboard=[
    [dict(text='انصراف')],[dict(text='درباره رباتساز 🤖'), KeyboardButton(text='بازگشت'), KeyboardButton(text='خروج')]
    ])
"""    
inline_markup4chseller = InlineKeyboardMarkup(inline_keyboard = [
    [dict(text = 'ویرایش️', callback_data = ("E"+kwargs["title"])),
    InlineKeyboardButton(text = 'حذف', callback_data = ("D"+kwargs["title"])),
    InlineKeyboardButton(text = text_Flag4XF, callback_data = (Flag4XF + kwargs["title"]))]])
"""

async def seller_stage_func(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    user_id_token = str(user_id) + token
    sellers = seller_dict[user_id_token]
    if Intrance == 'خروج' :
        try:
            if user_id_token in seller_stage:
                del seller_stage[user_id_token]
            if token in close_store:
                bot.sendMessage(user_id, Start_New_Bot, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
            else:
                bot.sendMessage(user_id, Start_New_Bot, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))
            owner_stage[user_id_token] = "botsetting"
            if user_id_token in seller_stage:
                del seller_stage[user_id_token]
        except:
            pass
    elif Intrance == 'بازگشت':
        sellers = seller_dict[user_id_token]
        show_sellers = "لیست یوزرنیم فروشندگان: \n"
    
        if sellers:
            seller_keys = markup4seller
            for seller in sellers:
                if seller[1] != None:
                    show_sellers += "@" + seller[1] + "\n"
    
        else:
            seller_keys = markup4noseller
            show_sellers = "فروشنده ای معرفی نشده است. \n لطفا فروشنده معرفی نمایید."
        try:
            bot.sendMessage(user_id, show_sellers, reply_markup = seller_keys)
            owner_stage[user_id_token] = "seller_stage"
            del seller_stage[user_id_token]
        except:
            pass
    elif Intrance == "درباره رباتساز 🤖":
        try:
            bot.sendMessage(user_id, Tabligh)        
        except:
            pass
     
    elif Intrance == 'معرفی فروشنده' and user_id_token not in seller_stage:
        try:
            bot.sendMessage(user_id, characterseller, reply_markup = markup4chseller)
        except:
            pass
        seller_stage[user_id_token] = "Seller_Endorsement"

    elif Intrance == 'حذف فروشنده' and user_id_token not in seller_stage:
        try:
            bot.sendMessage(user_id, sellerdeletion, reply_markup = InlineKeyboardMarkup(inline_keyboard = await func_markupseller(file_name, user_id_token)))
        except:
            pass
    
    elif Input_Control == "data":
        seller_counter = 0
        for seller in sellers:
            if Intrance == "deletioncancelled":
                try:
                    bot.editMessageText(message_id, seller_deletion_cancelled)
                except:
                    pass
            elif seller[1] == Intrance[2:]:
                await sellerdb("delete_seller", seller_uid = Intrance[2:], tablenumber = file_name)
                del seller_dict[user_id_token][seller_counter]
                try:
                    bot.editMessageText(message_id, seller_deleted)
                except:
                    pass
                break
            seller_counter += 1
                
    elif user_id_token in seller_stage and seller_stage[user_id_token] == "Seller_Endorsement":
        if Intrance == 'انصراف':
            sellers = seller_dict[user_id_token]
            show_sellers = "لیست یوزرنیم فروشندگان: \n"
            if sellers:
                seller_keys = markup4seller
                for seller in sellers:
                    if seller[1] != None:
                        show_sellers += "@" + seller[1] + "\n"
            else:
                seller_keys = markup4noseller
            try:
                bot.sendMessage(user_id, show_sellers, reply_markup = seller_keys)
            except:
                pass
            owner_stage[user_id_token] = "seller_stage"
            del seller_stage[user_id_token]

        else:
            if Intrance[:1] == "@":
                Intrance = Intrance[1:]
            await sellerdb("Seller_Endorsement", seller_uid = Intrance, tablenumber = file_name)
            seller_dict[user_id_token].append([None, Intrance])
            try:
                bot.sendMessage(user_id, seller_saved_indb, reply_markup = markup4seller)
            except:
                pass
    else:
        try:
            bot.sendMessage(user_id, Tabligh)
        except:
            pass

async def func_markupseller(file_name, user_id_token):
    sellers = seller_dict[user_id_token]
    list4seller = []
    for seller in sellers:
        if seller[1] != None:        
            list4seller.append([dict(text = "@" + seller[1], callback_data = "ok" + seller[1])])
    list4seller.append([dict(text = 'انصراف', callback_data = "deletioncancelled")])
    return list4seller
