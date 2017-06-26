import sys
import asyncio
import telepot
import telepot.aio
import aiomysql

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from . import MessageTexts

from .Bugs import Test_Token, is_int
from .db_takjoy import db4takjoy
from .Simple import *


async def chek_username_indb(Intrance):
    temp = MessageTexts.UNT_Dict
    for i in range(1,len(temp)):
        if temp[i][1] == Intrance:
            return True
    else:
        return False        

       

async def check_username_token(user_id):
    
    unt_temp = MessageTexts.UNT_Dict
    for UN_key in dict.keys(unt_temp):
        if unt_temp[UN_key][0] == user_id:
            my_UNT = unt_temp[UN_key][2]
            Temp4UN.append(my_UNT)
            my_token = unt_temp[UN_key][1]
            Temp4UN.append(my_token)
            UNT_result[my_UNT]=my_token
    return UNT_result
    


class username():

    def __inite__(self , bot):
        self.bot = bot
        
    def check_username_intrance():
        loop = asyncio.get_event_loop()

        loop.create_task(self.bot.message_loop(UI))

        loop.run_forever()

