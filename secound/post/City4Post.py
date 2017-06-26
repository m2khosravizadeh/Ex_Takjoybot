import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .city4post_constants import *
from ..secound_constants import *
from ..all_funcs import *
from ...first.db_takjoy import db4takjoy

async def city4post_stage(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    user_id_token = str(user_id) + token
    markup4give_city_name = ReplyKeyboardMarkup(keyboard=[
                            [dict(text='انصراف'), KeyboardButton(text='درباره رباتساز 🤖')] , [dict(text='خروج'), KeyboardButton(text='بازگشت')],
                            ])
    def relinquishment():
        if user_id_token in ctrl_citydict:
            del ctrl_citydict[user_id_token]
        if user_id_token in city4postdict:
            del city4postdict[user_id_token]
        try:
            bot.sendMessage(user_id, cancelled + createoreditcity4post, reply_markup = AEcitypostkeys)
        except:
            pass
    if user_id_token not in ctrl_citydict:
        ctrl_citydict[user_id_token] = "ADD_New"
    if Intrance == "افزودن" and ctrl_citydict[user_id_token] == "ADD_New":
        try:
            bot.sendMessage(user_id, give_city_name, reply_markup = markup4give_city_name)
        except:
            pass
        ctrl_citydict[user_id_token] = 'give_city_name'
    elif Intrance == "ویرایش":
        posts = await db4takjoy('db4citypost',ctrl_account = 'take_from_citypost',table_name = file_name)
        try:
            if posts:
                bot.sendMessage(user_id, post_edition, reply_markup = InlineKeyboardMarkup(inline_keyboard = 
                await func_markup_post(file_name, user_id_token,posts, "Edt")))
            else:
                bot.sendMessage(user_id, post_not_exists)
        except:
            pass
    elif Intrance == "حذف":
        posts = await db4takjoy('db4citypost',ctrl_account = 'take_from_citypost',table_name = file_name)
        try:
            if posts:
                bot.sendMessage(user_id, post_deletion, reply_markup = InlineKeyboardMarkup(inline_keyboard = 
                await func_markup_post(file_name, user_id_token, posts, "Dlt")))
            else:
                bot.sendMessage(user_id, post_not_exists)
        except:
            pass
    elif Input_Control == "data":
        seller_counter = 0
        posts = await db4takjoy('db4citypost',ctrl_account = 'take_from_citypost',table_name = file_name)
        if Intrance[:2] == "ca":
            try:
                bot.editMessageText(message_id, post_edition_cancelled)
            except:
                pass
        elif Intrance[:2] == "ok":
            for post in posts:
                if post[0].decode('utf8') == Intrance[5:]:
                    if Intrance[2:5] == "Dlt":
                        await db4takjoy('db4citypost',ctrl_account = 'delete_citypost',table_name = file_name, city_name = Intrance[5:])
                        for citybox in dict_citypost[file_name]:
                            if citybox[0] == Intrance[5:]:
                                dict_citypost[file_name].remove([citybox[0], citybox[1]])
                                break
                        del ctrl_citydict[user_id_token]
                        try:
                            bot.editMessageText(message_id, city_deleted_successfully)
                        except:
                            pass
                    elif Intrance[2:5] == "Edt":
                        try:
                            bot.editMessageText(message_id, give_new_city_name)
                        except:
                            pass
                        ctrl_citydict[user_id_token] = 'give_city_name4edit'
                        ex_city[user_id_token] = Intrance[5:]

    elif ctrl_citydict[user_id_token] == 'give_city_name4edit':
        city4postedit[user_id_token] = Intrance
        try:
            bot.sendMessage(user_id, give_purchaseofcity)
        except:
            pass
        ctrl_citydict[user_id_token] = 'give_purchaseofcity4edit'
    elif ctrl_citydict[user_id_token] == 'give_purchaseofcity4edit':
        if Intrance.isdigit():
            await db4takjoy("db4citypost", ctrl_account = "edit_citypost", ex_city_name = ex_city[user_id_token], city_name = city4postedit[user_id_token], purchaseofcity = Intrance, table_name = file_name)
            try:
                bot.sendMessage(user_id, purchase_added + "\n" + createoreditcity4post, reply_markup = AEcitypostkeys)
            except:
                pass
            for citybox in dict_citypost[file_name]:
                if citybox[0] == city4postedit[user_id_token]:
                    dict_citypost[file_name].remove([citybox[0],citybox[1]])
                    dict_citypost[file_name].append([citybox[0], Intrance])
                    break
            else:
                dict_citypost[file_name].append([city4postedit[user_id_token], Intrance])
            del city4postedit[user_id_token]
            del ctrl_citydict[user_id_token]
        elif Intrance == "انصراف":
            relinquishment()
        else:
            try:
                bot.sendMessage(user_id, give_purchaseofcity)
            except:
                pass
    elif ctrl_citydict[user_id_token] == 'give_city_name':
        if Intrance == "انصراف":
            relinquishment()
        else:
            city4postdict[user_id_token] = Intrance
            try:
                bot.sendMessage(user_id, give_purchaseofcity)
            except:
                pass
            ctrl_citydict[user_id_token] = 'give_purchaseofcity'
    elif ctrl_citydict[user_id_token] == 'give_purchaseofcity':
        if Intrance.isdigit():
            await db4takjoy("create_db4citypost", city_name = city4postdict[user_id_token], post_purchase = Intrance, table_name = file_name)
            try:
                bot.sendMessage(user_id, purchase_added, reply_markup = AEcitypostkeys)
            except:
                pass
            for citybox in dict_citypost[file_name]:
                if citybox[0] == city4postdict[user_id_token]:
                    dict_citypost[file_name].remove([citybox[0], citybox[1]])
                    dict_citypost[file_name].append([citybox[0], Intrance])
                    break
            else:
                dict_citypost[file_name].append([city4postdict[user_id_token], Intrance])
                        
            del ctrl_citydict[user_id_token]
            del city4postdict[user_id_token]
        elif Intrance == "انصراف":
            relinquishment()
        else:
            try:
                bot.sendMessage(user_id, give_purchaseofcity)
            except:
                pass
    elif Intrance == "انصراف":
        relinquishment()

    elif Intrance == "خروج":
        try:
            del ctrl_citydict[user_id_token]
            del city4postdict[user_id_token]
        except:
            pass
        owner_stage[user_id_token] = "botsetting"
        blu = common_func(Intrance, bot, user_id, token)        
    elif Intrance == "بازگشت":
        try:
            del ctrl_citydict[user_id_token]
            del city4postdict[user_id_token]
        except:
            pass
        if ctrl_citydict[user_id_token] == 'give_purchaseofcity':
            try:
                bot.sendMessage(user_id, give_city_name, reply_markup = markup4give_city_name)
            except:
                pass
            ctrl_citydict[user_id_token] = 'give_city_name'
        elif ctrl_citydict[user_id_token] == 'give_city_name':
            owner_stage[user_id_token] = "botsetting"
            blu = common_func(Intrance, bot, user_id, token)        
    else:
        try:
            bot.sendMessage(user_id, Tabligh)
        except:
            pass

async def func_markup_post(file_name, user_id_token, posts, ctrl4ED):
    list4post = []
    for post in posts:
        if post[1] != None:        
            list4post.append([dict(text = post[0].decode("utf8") , callback_data = "ok" + ctrl4ED + post[0].decode("utf8"))])
    list4post.append([dict(text = 'انصراف', callback_data = "ca" + ctrl4ED)])
    return list4post
