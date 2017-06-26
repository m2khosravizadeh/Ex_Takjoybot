import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='راهنمایی') , KeyboardButton(text='پشتیبانی')], [dict(text='درباره رباتساز'), KeyboardButton(text='تنظیمات')],
    ])

def result4show(chat_id, bot, user_id_token,**kwargs):

    if kwargs["show_photo_file"]:

        bot.sendPhoto(chat_id, kwargs["show_photo_file"])
        
    bot.sendMessage(chat_id, kwargs["show_title"])
    if kwargs["show_context"] is not None :

        bot.sendMessage(chat_id, kwargs["show_context"])

    if kwargs["show_price_ware"] is not None:

        bot.sendMessage(chat_id, "قیمت: " + str(kwargs["show_price_ware"]) + " " + str(kwargs["show_currency_ware"]))

    if kwargs["show_discount"] is not None:

        bot.sendMessage(chat_id, "تخفیف: " + kwargs["show_discount"] + "درصد")
        final_price = str(int((100 - int(kwargs["show_discount"])) * int(kwargs["show_price_ware"])/100))
        bot.sendMessage(chat_id, "قیمت نهایی: " + final_price+ " " + str(kwargs["show_currency_ware"]))

    
