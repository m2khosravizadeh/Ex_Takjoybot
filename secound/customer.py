import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .customer_constants import *
from .secound_constants import *
from ..first.db_takjoy import db4takjoy
from ..Third.Third_constants import *

async def customerfunc(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    customer_id = Intrance[1:10]
    customer_code = Intrance[11:]
    customer_token = customer_id + token
    inline_markup4seller_mistake = InlineKeyboardMarkup(inline_keyboard = [[dict(text='بله، مطمئنم', callback_data = "CustomerRefused"),
                                                                            dict(text='نه، اشتباه شد. بپذیر.', callback_data = "CustomerY" + Intrance[1:])]])
    inline_markup4bill_payment = InlineKeyboardMarkup(inline_keyboard = [[dict(text='ارسال فیش', callback_data = "bill_payment" + Intrance[1:])],
                                                                         [dict(text='انصراف', callback_data = "bill_cancel0" + Intrance[1:])]])
                                                                         
    markup4seller_simple = ReplyKeyboardMarkup(keyboard=[[dict(text='درباره رباتساز 🤖')]],resize_keyboard = True)

    if Intrance[0] == "Y":
        try:
            result_all_account = await db4takjoy('account_db', ctrl_account = "take_all_from_db", table_num = file_name)
            bot.sendMessage(customer_id, purchase_accepted_by_seller, reply_markup = markup4seller_simple)
            if customer_token in purchase_citypost:
                message2customer = ''
                for accounts in result_all_account:
                    message2customer += accounts[0].decode('utf8') + ' به نام: ' + accounts[1].decode('utf8') + "\n"
                bot.sendMessage(customer_id, pay_price.format(price = str(int(Total_price_dict[customer_token]) + int(purchase_citypost[customer_token]))) 
                                             + "\n\n" + message2customer + "\n 🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻 \n" 
                                             + pay_attention_pay_price, reply_markup = inline_markup4bill_payment)
            bot.editMessageText(message_id, customer_order_characteristic[Intrance[1:]] + purchase_accepted_by_seller)
        except:
            pass
    elif Intrance[0] == "N":
        try:
            bot.sendMessage(customer_id, check_mistake_seller, reply_markup = inline_markup4seller_mistake)
        except:
            pass
    elif Intrance[:5] == "Final":
        if Intrance[5:7] == "ok":
            customer_id = Intrance[7:16]
            try:
                bot.sendMessage(customer_id, final_acception_message)
            except:
                pass
        elif Intrance[5:12] == "refused":
            try:
                customer_id = Intrance[12:21]
                bot.sendMessage(customer_id, final_refused_message)
            except:
                pass

