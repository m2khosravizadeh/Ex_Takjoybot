import asyncio
import telepot

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from . import MessageTexts

class Test_Token():
    def __init__(self, Token, USERID):
        self.USERID = USERID
        self.Token = Token
        
    def OK(self):
        markup = ReplyKeyboardMarkup(keyboard=[
	[dict(text='تنظیمات') , KeyboardButton(text='راهنمایی')],
	[dict(text='پشتیبانی') , KeyboardButton(text='درباره رباتساز')],
	])
        try:

            mybot = telepot.Bot(self.Token)
            mybot.sendMessage(self.USERID, MessageTexts.Welcome2urBot, reply_markup=markup)
            mybot.sendMessage(self.USERID, MessageTexts.Tabligh)

            return True
        except:
            return False

def is_int(value):
    try:
        return isinstance(int(value),int)
    except:
        return False

