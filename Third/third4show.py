import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .db_others import db4other
   
async def show_result(chat_id, bot, user_id_token, markup_key = None, ex_key = None, *sh4c, **kwargs):
    inline_markup = None
    if "title" in kwargs:
        inline_markup = InlineKeyboardMarkup(inline_keyboard = [[dict(text='سفارش️', callback_data = kwargs["title"])]])
    Show2customer = ""
    markup = ReplyKeyboardMarkup(keyboard = markup_key, resize_keyboard = True)
    if ex_key:
        try:
            bot.sendMessage(chat_id, ex_key + ":", reply_markup = markup)
        except:
            pass
        if "title" in kwargs:
            Show2customer += kwargs["title"] + "\n\n"
    else:
        try:
            bot.sendMessage(chat_id, kwargs["title"], reply_markup = markup)
        except:
            pass

    if "file_id" in kwargs:
        try:
            bot.sendPhoto(chat_id, kwargs["file_id"])
        except:
            pass

    if "context" in kwargs:
        Show2customer += kwargs["context"] + "\n\n"

    if "price_ware" in kwargs:
        file_name = kwargs["File_name"] 
        Show2customer += "قیمت: " + kwargs["price_ware"] + " " + kwargs["currency_ware"] + "\n\n"
        Tiscon = await db4other("Title_Check", table_name = file_name)
        if Tiscon and "discount" not in kwargs:
            for First_Tiscon in Tiscon:
                if kwargs["title"] == First_Tiscon[0].decode('utf8'):
                    try:
                        bot.sendMessage(chat_id, Show2customer + "\n ☘🍁☘🍁☘🍁☘🍁☘ \n" + " تمام شد. ")
                    except:
                        pass
                    break
            else:
                try:
                    bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)
                except:
                    pass                
        elif "discount" not in kwargs:
            try:
                bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)
            except:
                pass

    if "discount" in kwargs:
        Show2customer += "تخفیف: " + kwargs["discount"] + "درصد \n"
        final_price = str(int((100 - int(kwargs["discount"])) * int(kwargs["price_ware"])/100))
        Show2customer += "قیمت نهایی: " + final_price + " " + kwargs["currency_ware"] + "\n\n"
        file_name = kwargs["File_name"] 
        Tiscon = await db4other("Title_Check",table_name = file_name)
        if Tiscon:
            for First_Tiscon in Tiscon:
                if kwargs["title"] == First_Tiscon[0].decode('utf8'):
                    try:
                        bot.sendMessage(chat_id, Show2customer + "\n ☘🍁☘🍁☘🍁☘🍁 \n" + " تمام شد. ")
                    except:
                        pass
                    break
            else:
                try:
                    bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)
                except:
                    pass
        else:
            try:
                bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)
            except:
                pass

    elif "price_ware" not in kwargs and Show2customer:
        try:
            bot.sendMessage(chat_id, Show2customer)
        except:
            pass

def changezip(*sh4c):
    if len(sh4c) == 2:
        return "['"+str(sh4c[1])+"']"
    elif len(sh4c) == 4:
        return "['"+sh4c[1]+"','"+str(sh4c[3])+ "']"
    elif len(sh4c) == 6:
        return "['"+sh4c[1]+"','"+sh4c[3]+"','"+str(sh4c[5])+ "']"
