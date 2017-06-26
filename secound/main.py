import sys
import asyncio
import telepot
import telepot.aio
import aiomysql
import requests
import os
import shutil


from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .secound_constants import *


async def test(msg):
    try:
        flavor = telepot.flavor(msg)
        summary = telepot.glance(msg, flavor=flavor)
        content_type, chat_type, chat_id = telepot.glance(msg)
        await bot.sendMessage(chat_id, "testi")
    except:
        pass
    if content_type == "photo":
        try:
            my_file = msg['photo'][-1]['file_id']
            photo_file = await bot.getFile(msg['photo'][-1]['file_id'])
            file_path = photo_file['file_path']
            file_link = 'https://api.telegram.org/file/bot' + TOKEN + '/' + file_path
            getImage(file_link, folder = "./files/")
        except:
            pass

def _createFilename(url, name, folder, user_id_token):
    dotSplit = url.split('.')
    if name == None:
        slashSplit = dotSplit[-2].split('/')
        name = slashSplit[-1]
    ext = dotSplit[-1]
    file = '{}{}.{}'.format(folder, name, ext)
    return file

def getImage(url, name=None, folder='./', user_id_token = ""):
    myfile = _createFilename(url, name, folder, user_id_token)
    dic_photo_file[user_id_token] = myfile
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(myfile, 'wb') as f:
        r = requests.get(url, stream=True)
        for block in r.iter_content(1024):
            if not block:
                break
            f.write(block)



def getImageFast(url, name=None, folder='./'):
    file = createFilename(url, name, folder)
    r = requests.get(url)
    i = Image.open(StringIO(r.content))
    i.save(file)



def first_token():
    Bot_Token = ["183536666:AAHWrzN9vVKcrsr4OwPCu2r9WSEZR5ZqLDE", "247952700:AAG1CAj3fwo3KdBqUWkWsYGxRwYsjS7V7Vw"]
    while True:
        for i in range(0,2):
            global TOKEN
            TOKEN = Bot_Token[i]
            loop = asyncio.get_event_loop()
            global bot
            bot = telepot.aio.Bot(Bot_Token[i])
            loop.run_until_complete(bot.message_loop(test))
            loop.close


if __name__ == "__main__":
    first_token()
