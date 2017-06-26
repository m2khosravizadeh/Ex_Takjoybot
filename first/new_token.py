import sys
import asyncio
import telepot
import telepot.aio
import aiomysql

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .MessageTexts import *

from .Bugs import Test_Token, is_int

  
async def token_change(usernames):
    blinker = True
    result_token_change = "InlineKeyboardMarkup(inline_keyboard=["
    for username in dict.keys(usernames):
        print (username)
        if blinker:
            result_token_change +="[InlineKeyboardButton(text='{0}', callback_data='{1}')],".format(username,username)
            blinker = False
        else:
            result_token_change +="[InlineKeyboardButton(text='{0}', callback_data='{1}')],".format(username,username)
            blinker = True

    result_token_change += "])"
            
    print (eval(result_token_change))
        
    return (eval(result_token_change))

