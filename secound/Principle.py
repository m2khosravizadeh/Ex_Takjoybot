import asyncio
import traceback
import telepot
import telepot.aio
from datetime import datetime

from concurrent.futures import ProcessPoolExecutor

from .Owner import secound_stage
from .secound_constants import *
from .Seller.db4seller import sellerdb
from .Seller.const4seller import *
from ..first.db_takjoy import db4takjoy
from ..first.Simple import start_control, on_callback_query
from ..Third.main import third_stage

global let_update

Cwargs = {}
token_takjoy = None
"""
msg is:  {'message_id': 778,
'from': {'id': 132684196, 'last_name': '@takjoybot', 'first_name': 'پشتیبان اصلی', 'username': 'XtakjoyX'},
'text': 'خروج',
'chat': {'id': 132684196, 'last_name': '@takjoybot', 'first_name': 'پشتیبان اصلی', 'type': 'private', 'username': 'XtakjoyX'},
'date': 1493580942}
Chat: text private 132684196
getMe :  {'id': 358736838, 'first_name': 'رزومه محمد خسروی زاده', 'username': 'm2khosravizadeh_bot'}
"""

def main(token_takjoy):
    #global token_takjoy
    #token_takjoy = par_token_takjoy
    BOT = telepot.aio.Bot(token_takjoy)

    loop = asyncio.get_event_loop()

    print("in final main")

    async def first4chat(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(10 * "*", "in first4chat", 10 * '*', "\n"," msg is: ", msg)
        #temp_bot = await bot.getme()
        #token = dic_user_id_bot(temp_bot["username"])
        fargs = {"username": msg["from"]["username"]}
        if chat_type != "private":
            pass
        else:
            print("in start_control")
            await start_control(chat_id, msg['text'], content_type, _bot = BOT, **fargs)


    async def first4callback_query(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        #temp_bot = await bot.getme()
        #token = dic_user_id_bot(temp_bot["username"])
        msg_identifier = (chat_id, msg["message_id"])
        if chat_type != "private":
            pass
        else:
            await on_callback_query(chat_id, msg_identifier, BOT, msg["text"], **Cwargs)

    task = asyncio.ensure_future(BOT.message_loop({'chat': first4chat,
                          'callback_query': first4callback_query}, allowed_updates=["message"]))
    tasks.append(task)
    for my_number in UNT_Dict:
        TOKEN = UNT_Dict[my_number][1]
        print("token is: ", TOKEN)
        #TOKEN2my_number[TOKEN] = my_number
        sem = asyncio.Semaphore(1000)
        task = asyncio.ensure_future(bot_ctrl_chat(TOKEN, sem, UNT_Dict[my_number][0], my_number))
        #user_id_owner[TOKEN] = UNT_Dict[my_number][0]

        tasks.append(task)
    print("tasks is: ", tasks)
    asyncio.gather(*tasks)
    loop.run_forever()

"""
class takjoy_ctrl(token_takjoy):
    pass
"""

async def bot_ctrl_chat(token, sem, user_id_owner, my_number,*args, **kwargs):
    print("in main class: \n", token, "\n", sem)
    #async with self.sem:
    bot = telepot.Bot(token)
    BOT = telepot.aio.Bot(token)
    print("bot is:", BOT)
    """
    await BOT.message_loop({'chat': notfirst4chat,
                                'callback_query': notfirst4callback_query})
    """
    print("mistake")
    async def notfirst4chat(msg):
        print("in notfirst4chat msg")
        content_type, chat_type, chat_id = telepot.glance(msg)
        #temp_user_id_owner = await common_func(bot)
        msg_identifier = (chat_id, msg["message_id"])
        if chat_type != "private":
            pass
        else:
            if chat_id == user_id_owner:
                kwargs2 = {"sellerfalg":False, "message_id":msg_identifier}
            else:
                kwargs2 = {"sellerfalg":True, "message_id":msg_identifier}
            if "username" in msg["from"]:
                un = msg["from"]["username"]
            else:
                un = None
            flag4seller = await check_username_in_seller_or_owner(chat_id, un, user_id_owner)
            if str(chat_id) == user_id_owner or flag4seller:
                await secound_stage(chat_id, token, msg["text"], content_type, bot, my_number, **kwargs2)
            else:
                test_close_or_time(token, chat_id, my_number)
                await third_stage(chat_id, token, msg["text"], content_type, bot, my_number, message_id = msg_identifier)


    async def notfirst4callback_query(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        #temp_user_id_owner = await common_func(bot)
        msg_identifier = (chat_id, msg["message_id"])
        kwargs2 = {"sellerfalg":False, "message_id":msg_identifier}
        if chat_id == user_id_owner:
            kwargs2 = {"sellerfalg":False, "message_id":msg_identifier}
        else:
            kwargs2 = {"sellerfalg":True, "message_id":msg_identifier}
        if chat_type != "private":
            pass
        else:
            if str(chat_id) == user_id_owner:
                await secound_stage(chat_id, token, msg["text"], content_type, bot, my_number, **kwargs2)
            else:
                await test_close_or_time(token, chat_id, my_number)
                await third_stage(chat_id, token, msg["text"], content_type, bot, my_number, message_id = msg_identifier)
    print("notfirst4chat is:")


    async def check_username_in_seller_or_owner(user_id, username, user_id_owner):
        username_in_seller_list = False
        for seller_list in seller_dict[user_id_owner + token]:
            if username == seller_list[1]:
                username_in_seller_list = True
                if user_id and str(user_id) != seller_list[0]:
                    seller_list[0] = str(user_id)
                    await sellerdb('update_seller_id', seller_uid = username, seller_value = str(user_id), tablenumber = my_number)
                    break
            if user_id and str(user_id) == seller_list[0]:
                username_in_seller_list = True
                if username != seller_list[1]:
                    seller_list[0] = str(user_id)
                    await sellerdb('update_seller_name', seller_uid = username, seller_value = str(user_id), tablenumber = my_number)
                    break
        return username_in_seller_list


    async def test_close_or_time(token,user_id, my_number):
        if token in close_store or UNT_Dict[my_number][2] < datetime.now():
            try:
                await BOT.sendMessage(user_id, store_closed)
            except:
                return
        else:
            return

    async with sem:
        await BOT.message_loop({'chat': notfirst4chat,
                                'callback_query': notfirst4callback_query,
                              }, allowed_updates=["message"])

    """
    async def common_func(self, mybot):
        #temp_bot = await mybot.getme()
        #token = dic_user_id_bot[temp_bot["username"]]
        temp_user_id_owner = user_id_owner[self.token]
        return temp_user_id_owner
    """


"""
    msg_identifier = None
    offset = {}
    let_update = {}
    bot = {}
    BOT = {}
    Cwargs = {}
    offset[token_takjoy] = None
    let4send_signal = True
    check_speed = 0
    temp_check = None
    while True:
        check_speed += 1
        if not temp_check:
            temp_check = datetime.now().minute
        if int(datetime.now().minute) - int(temp_check) == 1:
            print("check_speed is: ", check_speed)
            temp_check = datetime.now().minute

        loop = asyncio.get_event_loop()
        bot[token_takjoy] = telepot.Bot(token_takjoy)
        BOT[token_takjoy] = telepot.aio.Bot(token_takjoy)
        if token_takjoy not in token_takjoy_bot:
            token_takjoy_bot.append(token_takjoy)
        try:
            result_token_takjoy = bot[token_takjoy].getUpdates(offset = offset[token_takjoy])
            if result_token_takjoy:
                username = user_id = Intrance = ""
                update_id0 = result_token_takjoy[0]['update_id']
                offset[token_takjoy] = int(update_id0) + 1
                if "message" in result_token_takjoy[0]:
                    user_id = result_token_takjoy[0]["message"]["chat"]["id"]
                    if "username" in result_token_takjoy[0]["message"]["chat"]:
                        username = result_token_takjoy[0]["message"]["chat"]["username"]
                    if "text" in result_token_takjoy[0]["message"]:
                        Intrance = result_token_takjoy[0]["message"]["text"]
                        Input_Control = "text"
                        fargs = {"username" : username}
                        await start_control(user_id, Intrance, Input_Control, _bot = BOT[token_takjoy], **fargs)
                elif 'callback_query' in result_token_takjoy[0]:
                    user_id4takjoy = result_token_takjoy[0]["callback_query"]["message"]["chat"]["id"]
                    if "username" in result_token_takjoy[0]["callback_query"]["message"]["chat"]:
                        username4takjoy = result_token_takjoy[0]["callback_query"]["message"]["chat"]["username"]
                    message_id = result_token_takjoy[0]["callback_query"]["message"]["message_id"]
                    user_id_token = str(user_id4takjoy) + TOKEN
                    msg_identifier = (user_id4takjoy, message_id)
                    Intrance = result_token_takjoy[0]["callback_query"]["data"]
                    await on_callback_query(user_id4takjoy, msg_identifier, BOT[token_takjoy], Intrance, **Cwargs)

        except:
            traceback.print_exc()

        for my_number in UNT_Dict:
            TOKEN = UNT_Dict[my_number][1]

            if TOKEN not in offset:
                offset[TOKEN] = 0
            if TOKEN not in bot:
                bot[TOKEN] = None

            bot[TOKEN] = telepot.Bot(TOKEN)
            BOT[TOKEN] = telepot.aio.Bot(TOKEN)
            result = []
            try:
                result = bot[TOKEN].getUpdates(offset = offset[TOKEN])
            except:
                pass

            if result:
                print("result is: ", result)
                username = user_id = Intrance = ""
                update_id1 = result[0]['update_id']
                offset[TOKEN] = int(update_id1) + 1
                if "message" in result[0]:
                    user_id = result[0]["message"]["chat"]["id"]
                    if "username" in result[0]["message"]["chat"]:
                        username = result[0]["message"]["chat"]["username"]

                    if "photo" in result[0]["message"]:
                        Intrance = result[0]["message"]["photo"][-1]['file_id']
                        Input_Control = "photo"
                        msg_identifier = result[0]["message"]["message_id"]

                    elif "text" in result[0]["message"]:
                        Intrance = result[0]["message"]["text"]
                        Input_Control = "text"

                elif 'callback_query' in result[0]:
                    user_id = result[0]["callback_query"]["message"]["chat"]["id"]
                    if "username" in result[0]["callback_query"]["message"]["chat"]:
                        username = result[0]["callback_query"]["message"]["chat"]["username"]
                    message_id = result[0]["callback_query"]["message"]["message_id"]
                    user_id_token = str(user_id) + TOKEN
                    msg_identifier = (user_id, message_id)
                    Intrance = result[0]["callback_query"]["data"]
                    Input_Control = "data"
                user_id_owner = UNT_Dict[my_number][0]
                if user_id and int(user_id) > 0 and (str(user_id) + TOKEN) not in flag4mine:
                    bot_intrance = bot[TOKEN].getMe()
                    for my_user_id in my_user_ids:
                        bot[token_takjoy].sendMessage(my_user_id, dude_comes.format(username = username,
                        bot = bot_intrance["username"], u_id = str(user_id))),

                    flag4mine.append(str(user_id) + TOKEN)
                if user_id and int(user_id) > 0 and str(user_id) == user_id_owner and Intrance:
                    kwargs2 = {"sellerfalg":False, "message_id":msg_identifier}
                    if str(user_id)+ TOKEN not in seller_const4show:
                        seller_const4show.append(str(user_id)+ TOKEN)
                    await secound_stage(user_id, TOKEN, Intrance, Input_Control, bot[TOKEN], my_number, **kwargs2)

                elif user_id and int(user_id) > 0:
                    username_in_seller_list = False
                    for seller_list in seller_dict[user_id_owner + TOKEN]:
                        if username == seller_list[1]:
                            username_in_seller_list = True
                            if user_id and str(user_id) != seller_list[0]:
                                seller_list[0] = str(user_id)
                                await sellerdb('update_seller_id', seller_uid = username, seller_value = str(user_id), tablenumber = my_number)
                                break
                        if str(user_id) == seller_list[0]:
                            username_in_seller_list = True
                            if username != seller_list[1]:
                                seller_list[0] = str(user_id)
                                await sellerdb('update_seller_name', seller_uid = username, seller_value = str(user_id), tablenumber = my_number)
                                break
                    if username_in_seller_list and Intrance:
                        kwargs2 = {"sellerfalg":True, "message_id":msg_identifier}
                        await secound_stage(user_id, TOKEN, Intrance, Input_Control, bot[TOKEN], my_number, **kwargs2)

                    else:
                        if TOKEN in close_store:
                            try:
                                bot[TOKEN].sendMessage(user_id, store_closed)
                            except:
                                pass
                        elif UNT_Dict[my_number][2] < datetime.now():
                            try:
                                bot[TOKEN].sendMessage(user_id, store_closed)
                            except:
                                pass
                        elif Intrance:
                            await third_stage(user_id, TOKEN, Intrance, Input_Control, bot[TOKEN], my_number, message_id = msg_identifier)
                if user_id_owner and int(user_id_owner) > 0:
                    user_id4owner[TOKEN] = user_id_owner + TOKEN
        if let4send_signal and datetime.now().minute < 2:
            let4send_signal = False
            for my_user_id in my_user_ids:
                bot[token_takjoy].sendMessage(my_user_id, botmaker_works.format(sec = str(int(int(check_speed)/3600)), mine = str(int(int(check_speed)/60))))
                check_speed = 0
        elif not let4send_signal and datetime.now().minute > 2:
            let4send_signal = True

"""
if __name__ == "__main__":
    main()


