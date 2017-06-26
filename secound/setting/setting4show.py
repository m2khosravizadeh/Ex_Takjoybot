import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .setting_constants import *
global flag4editmessage
flag4editmessage = False

def show_edited (chat_id, bot, user_id_token, message_id, Flag4XF, markup_key = None ,*sh4c, **kwargs):

    chatid = message_id
    global flag4editmessage
    flag4editmessage = True
    show_result(chatid, bot, user_id_token, Flag4XF, markup_key, None, *sh4c, **kwargs)
    
def show_result(chat_id, bot, user_id_token, Flag4XF, markup_key = None, ex_key = None, *sh4c, **kwargs):
    global flag4editmessage

    Show2customer = ""
    markup = ReplyKeyboardMarkup(keyboard=markup_key)
    if Flag4XF == "X":
        text_Flag4XF = "اتمام"
    elif Flag4XF == "F":
        text_Flag4XF = "موجود است"

    if not flag4editmessage:
        
        if not ex_key:
            if sh4c[-1] == 0:
                ex_key = tnxfromseller + pluskeymessage + menuskeymessage + editkeymessage + newproductkey
            else:
                ex_key = next_product
        else:
            ex_key += ":"    
        try:
            bot.sendMessage(chat_id, ex_key , reply_markup = markup)
        except:
            pass

    if kwargs:
        if "price_ware" in kwargs:
            inline_markup = InlineKeyboardMarkup(inline_keyboard = [
                                                 [dict(text = 'ویرایش️', callback_data = ("E"+kwargs["title"])),
                                                 InlineKeyboardButton(text = 'حذف', callback_data = ("D"+kwargs["title"])),
                                                 InlineKeyboardButton(text = text_Flag4XF, callback_data = (Flag4XF + kwargs["title"]))]])
        
        else:
            inline_markup = InlineKeyboardMarkup(inline_keyboard = [
                                                 [dict(text = 'ویرایش️', callback_data = ("E"+kwargs["title"])),
                                                 InlineKeyboardButton(text = 'حذف', callback_data = ("D"+kwargs["title"]))]])
        Show2customer += kwargs["title"] + "\n\n"
        if "file_id" in kwargs and not flag4editmessage:
            try:
                bot.sendPhoto(chat_id, kwargs["file_id"])
            except:
                pass
        if "context" in kwargs:
            Show2customer += kwargs["context"] + "\n\n"

        if "price_ware" in kwargs:
            Show2customer += "قیمت: " + kwargs["price_ware"] + " " + kwargs["currency_ware"] + "\n"

        if "discount" in kwargs:
            Show2customer += "تخفیف: " + kwargs["discount"] + "درصد \n"
            final_price = str(int((100 - int(kwargs["discount"])) * int(kwargs["price_ware"])/100))
            
            Show2customer += "قیمت نهایی: " + final_price + " " + kwargs["currency_ware"] + "\n\n"
            try:
                if not flag4editmessage:
                    bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)                    
                else:
                    flag4editmessage = False
                    bot.editMessageText(chat_id, Show2customer, reply_markup = inline_markup)
            except:
                pass
        else:
            try:
                if not flag4editmessage:
                    bot.sendMessage(chat_id, Show2customer, reply_markup = inline_markup)
                else:
                    flag4editmessage = False                
                    bot.editMessageText(chat_id, Show2customer, reply_markup = inline_markup)
            except:
                pass
