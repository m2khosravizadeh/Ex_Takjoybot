import time
import asyncio
import traceback
import telepot
import telepot.aio


def handle(msg):
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("flavor is: ", flavor)
    print("summary is: ", summary)
    print("msg is: " , msg)
    
    
    chat_id = msg["chat"]["id"]
    Intrance = msg["text"]
    bot[token].sendMessage(chat_id,"testi")

    for i in range(0,3):
    let_update[token] = True
    loop.stop()
    

MYTOKEN = ["183536666:AAHWrzN9vVKcrsr4OwPCu2r9WSEZR5ZqLDE", "247952700:AAG1CAj3fwo3KdBqUWkWsYGxRwYsjS7V7Vw"]

offset = {}
bot = {}
answerer = {}
BOT = {}
while True:
    for TOKEN in MYTOKEN:
        loop = asyncio.get_event_loop()
        BOT[TOKEN] = telepot.aio.Bot(TOKEN)
        bot[TOKEN] = telepot.Bot(TOKEN)
        answerer[TOKEN] = telepot.helper.Answerer(bot[TOKEN])
        
        print(TOKEN,":",bot[TOKEN])
        bot[TOKEN].message_loop(handle)
        time.sleep(1)
            
            
