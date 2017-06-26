import time
import asyncio
import telepot
import telepot.aio

from .Account_constants import *
from ..all_funcs import *
from ...first.db_takjoy import db4takjoy

def func_markupaccount(*args):
    list4account = []
    for account in args:
        list4account.append([dict(text = account, callback_data = account)])
    else:
        list4account.append([dict(text = 'انصراف', callback_data = "deletioncancelled")])
    return list4account

async def account_number_func(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    user_id_token = str(user_id) + token
    def Exit_from_account():
        try:
            del account_dict[user_id_token]
            del account_number_dict[user_id_token]

        except:
            pass
        common_func('خروج', bot, user_id, token)

    if Intrance == 'درباره رباتساز 🤖':
        try:
            bot.sendMessage(user_id, Tabligh)
        except:
            pass
    elif Intrance == 'خروج':
        Exit_from_account()
    elif Intrance == 'بازگشت':
        try:
            bot.sendMessage(chat_id, choose_account_setting, reply_markup = AEcitypostkeys)
            del account_dict[user_id_token]
            del account_number_dict[user_id_token]
        except:
            pass
    elif Intrance == 'افزودن' and user_id_token not in account_dict:
        try:
            bot.sendMessage(user_id, give_number_account, reply_markup = markup_give_title)
            account_dict[user_id_token] = "give_new_account"
        except:
            pass
    elif Intrance == 'حذف' and user_id_token not in account_dict:
        result_account = await db4takjoy("account_db", ctrl_account = "take_from_db", table_num = file_name)
        try:
            if result_account:
                bot.sendMessage(user_id, give_account4deletion, reply_markup = InlineKeyboardMarkup(inline_keyboard = func_markupaccount(*result_account)))
            else:
                bot.sendMessage(user_id, you_have_no_account_number)
                Exit_from_account()
            account_dict[user_id_token] = "delete_account"
        except:
            pass
    elif user_id_token in account_dict and account_dict[user_id_token] == "give_new_account":
        try:
            if Intrance.isdigit():
                account_number_dict[user_id_token] = Intrance
                bot.sendMessage(user_id, give_account_owner_name)
                account_dict[user_id_token] = "give_account_owner_name"
            else:
                bot.sendMessage(user_id, give_number_account, reply_markup = markup_give_title)
        except:
            pass
    elif account_dict[user_id_token] == "delete_account" and Input_Control == "data":
        if Intrance.isdigit():
            await db4takjoy("account_db", ctrl_account = "Delete_from_db", table_num = file_name, account_num = Intrance)
            try:
                bot.editMessageText(message_id, account_deleted)
            except:
                pass
            Exit_from_account()
        elif Intrance == "deletioncancelled":
            try:
                bot.editMessageText(message_id, account_deletion_cancelled)
            except:
                pass
            Exit_from_account()
    elif account_dict[user_id_token] == "give_account_owner_name":
        await db4takjoy("account_db", ctrl_account = "save_in_db", 
        table_num = file_name, account_num = account_number_dict[user_id_token], account_name = Intrance)
        try:
            bot.sendMessage(user_id, account_saved)
        except:
            pass
        del account_number_dict[user_id_token]
        Exit_from_account()
    else:
        try:
            bot.sendMessage(user_id, Tabligh)
        except:
            pass
