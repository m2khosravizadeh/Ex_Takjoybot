import ast
import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from ..db4close_store import close_store_Funnc
from .setting_constants import *
from ..secound_constants import *
from .setting4show import show_result, show_edited
from .db_setting import db4other
from ..all_funcs import store_markup

markup4ch = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درست است') , KeyboardButton(text='آدرس'), KeyboardButton(text='مشخصات')],
    [dict(text='راهنمایی') , KeyboardButton(text='درباره رباتساز 🤖'), KeyboardButton(text='انصراف')],
    ])

markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='تعطیل 🔒'), KeyboardButton(text='تنظیمات ⚙'), KeyboardButton(text='درباره رباتساز 🤖')]])

markup_keyorbox = ReplyKeyboardMarkup(keyboard=[
    [dict(text='کلید') , KeyboardButton(text='محصول')],
    [dict(text='انصراف'), KeyboardButton(text='خروج')]
    ])
markup_give_title = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ])

markup_determent = ReplyKeyboardMarkup(keyboard=[[dict(text='انصراف')],
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج'), KeyboardButton(text='بازگشت')],
    ])

async def keymaker4pr(title):
    key_setting = InlineKeyboardMarkup(inline_keyboard = [
                                      [dict(text = 'نام محصول', callback_data = ("PRN" + title ))],
                                      [InlineKeyboardButton(text = 'متن', callback_data = ("PRT"+title))],
                                      [InlineKeyboardButton(text = 'عکس محصول', callback_data = ("PRP"+title))],
                                      [InlineKeyboardButton(text = 'قیمت محصول', callback_data = ("PRR"+title))],
                                      [InlineKeyboardButton(text = 'تخفیف', callback_data = ("PRC" + title))],
                                      [InlineKeyboardButton(text = 'انصراف', callback_data = ("det" + title))]])
    return key_setting

async def make_button(flag_NPE, flag_back = False, flag_next = False, *args):
    temp_markup = []

    markup_in = []
    counter_row = 0
    for keyboards in args:

        counter_row += 1
        if counter_row == 1:
            markup_in.append(dict(text = str(keyboards)))
        elif counter_row == 4:
            markup_in.append(KeyboardButton(text = keyboards))
            counter_row = 0
        else:
            markup_in.append(KeyboardButton(text = keyboards))
        if counter_row == 0:
            temp_markup.append(markup_in)
            markup_in = []
    else:
        if markup_in:
            temp_markup.append(markup_in)
            markup_in = []
        if flag_back:
            markup_in.append(dict(text = "بازگشت"))
        if flag_NPE != 6:
            markup_in.append(KeyboardButton(text = "+"))
            if args:
                markup_in.append(KeyboardButton(text = "ویرایش"))
                markup_in.append(KeyboardButton(text = "-"))
        else:
            markup_in.append(KeyboardButton(text = "محصول جدید"))
        markup_in.append(KeyboardButton(text = "درباره رباتساز 🤖"))
        markup_in.append(KeyboardButton(text = "خروج"))
        
        if flag_next:
            markup_in.append(KeyboardButton(text = "بعدی"))
        temp_markup.append(markup_in)

    return temp_markup


async def find_boxFrombox_dict(mytitle, **box):
    flag4notfinished = True
    counter4recursive = 0
    if "main" in box:
        for i in range(0, len(box["main"])):
            if mytitle == box["main"][i]["title"]:
                flag4notfinished = False

                return box["main"][i]
            if not flag4notfinished:
                break
    if "key" in box and flag4notfinished:
        counter4recursive += 1
        if counter4recursive < 3:
            for mykey in box["key"]:

                await find_boxFrombox_dict(mytitle, **box['key'][mykey]) 
        else:
            return None

async def setting_stage(user_id, token, Intrance, Input_Control, bot, file_name, message_id):
    user_id_token = str(user_id) + token
    BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)
    result_title = {}
    
    async def keyshowncancel_func():
        keys_with_cancel = await key_shown_cancel(False, False, *shown4customer[user_id_token])
        return ReplyKeyboardMarkup(keyboard=keys_with_cancel)

    async def common_check(Intrance, bot, chat_id, user_id_token):
        if Intrance == '/start' or Intrance == 'خروج':
            try:
                if token in close_store:
                    bot.sendMessage(chat_id, Start_New_Bot, reply_markup=store_markup("باز کردن 🔓", user_id_token = user_id_token))
                else:
                    bot.sendMessage(chat_id, Start_New_Bot, reply_markup=store_markup("تعطیل 🔒", user_id_token = user_id_token))
                owner_stage[user_id_token] = "botsetting"
                del shown4customer[user_id_token]
                return True
            except:
                pass
        elif Intrance == 'درباره رباتساز 🤖':
            try:
                bot.sendMessage(chat_id, Tabligh)        
                return True
            except:
                pass
        elif Intrance == '+' and len(shown4customer[user_id_token]) != 6:

            if user_id_token in dic_first_button:
                del dic_first_button[user_id_token]
            if user_id_token in dic_secound_button:
                del dic_secound_button[user_id_token]
            try:
                bot.sendMessage(chat_id, chosekeyorbox, reply_markup = markup_keyorbox)
                customer_stage[user_id_token] = "Add_chosen"
                return True
            except:
                pass
        elif Intrance == 'محصول جدید' and len(shown4customer[user_id_token]) == 6:

            dic_secound_button[user_id_token] = shown4customer[user_id_token][3]
            dic_first_button[user_id_token] = shown4customer[user_id_token][1]
            try:
                bot.sendMessage(user_id, give_title, reply_markup = markup_give_title)
                owner_stage[user_id_token] = "context"
                return True
            except:
                pass

        elif Intrance == 'ویرایش':
            markup_Editkey = await keyshowncancel_func()
            try:
                bot.sendMessage(chat_id, Editkey, reply_markup = markup_Editkey)
                customer_stage[user_id_token] = "Edit_chosen"
                return True
            except:
                pass
        elif Intrance == '-':
            markup_Deletkey = await keyshowncancel_func()
            try:
                bot.sendMessage(chat_id, deletekey, reply_markup = markup_Deletkey)
                customer_stage[user_id_token] = "Delete_chosen"
                return True
            except:
                pass
        else:
            return False
    
    async def makebutton4cancel(flag_NPE, flag_back = False, flag_next = False, *args):

        temp_markup = [[dict(text = "انصراف")]]


        markup_in = []
        counter_row = 0
        for keyboards in args:

            counter_row += 1
            if counter_row == 1:
                markup_in.append(dict(text = str(keyboards)))
            elif counter_row == 4:
                markup_in.append(KeyboardButton(text = keyboards))
                counter_row = 0
            else:
                markup_in.append(KeyboardButton(text = keyboards))
            if counter_row == 0:
                temp_markup.append(markup_in)
                markup_in = []
        else:
            if markup_in:
                temp_markup.append(markup_in)
        return temp_markup

    async def keyshown4cancel(flag_back = False, flag_next = False, *args):

        temp_key_shown = list(args)
        if len(temp_key_shown) == 2:

            key_shown = await makebutton4cancel(2, False, flag_next, *list(key_Box_Dict.keys()))
        elif len(temp_key_shown) == 4:
            key_shown = await makebutton4cancel(4, True, flag_next, *key_Box_Dict[temp_key_shown[1]])
        elif len(temp_key_shown) == 6:
            key_shown = await makebutton4cancel(6, True, flag_next)
        return key_shown

    async def keylimitationfunc(Input):
        if Input in canotuse4title:
            return False
        elif len(Input) > 15:
            return "longer"
        else:
            return "ok"

    def func_box(*args):

        temp4calc = BOX_Dict
        flag_temp4calc = True
        for i in range(0, len(args)-1):
            temp_in = temp4calc[args[i]]
            temp4calc = temp_in
        if args[-1] < len(temp4calc):

            return temp4calc[args[-1]]
        else:

            return {}

    async def key_shown_func(*args, flag_back = False, flag_next = False):
        temp_key_shown = list(args)
        if len(temp_key_shown) == 2:
            key_shown = await make_button(2, False, flag_next, *list(key_Box_Dict.keys()))
        elif len(temp_key_shown) == 4:

            key_shown = await make_button(4, True, flag_next, *key_Box_Dict[temp_key_shown[1]])
        elif len(temp_key_shown) == 6:

            key_shown = await make_button(6, True, flag_next)
        return key_shown

    async def key_shown_cancel(flag_back = False, flag_next = False, *args):

        temp_key_shown = list(args)
        if len(temp_key_shown) == 2:

            key_shown = await makebutton4cancel(2, False, flag_next, *list(key_Box_Dict.keys()))
        elif len(temp_key_shown) == 4:

            key_shown = await makebutton4cancel(4, True, flag_next, *key_Box_Dict[temp_key_shown[1]])
        elif len(temp_key_shown) == 6:

            key_shown = await makebutton4cancel(6, True, flag_next)
        return key_shown

    async def CheckIntranceInKeys(Intrance, *args):

        if len(args) == 2:
            if Intrance in list(key_Box_Dict.keys()):
                return True
            else:
                return False

        elif len(args) == 4:
            if Intrance in key_Box_Dict[args[1]]:
                return True
            else:
                return False

        else:
            return False

    async def Intrance2Box(Intrance):

        co_list = ast.literal_eval(customer_order[user_id_token])

        len_co = len(co_list)
        result_co = []
        for counter in range(0, len_co):

            temp_len_co = [middle_dic[2-counter], co_list[len_co - counter - 1]]
            result_co = temp_len_co + result_co

        result_co[-1] = int(result_co[-1])
        final_result = func_box(*result_co)
        return final_result

    def func_check_next(*args):

        temp = list(args)

        temp[-1] += 1
        box4next = func_box(*temp)
        if box4next:

            return True
        else:

            return False

    if user_id_token not in shown4customer:

        shown4customer[user_id_token] = ["main" , 0]

        key_shown = await make_button(2, False,bool(len(BOX_Dict['main']) > 1),*list(key_Box_Dict.keys()))
        temp_box4title = func_box(*shown4customer[user_id_token])

        result_title = await db4other("Product_Check", table_name = file_name)

        Flag4XF = "X"
        if result_title and "title" in temp_box4title:
            for first_result_title in result_title:
                if temp_box4title["title"] == first_result_title[0].decode("utf-8"):
                    Flag4XF = "F"
        customer_stage[user_id_token] = "first"
        box_show = {}
        if BOX_Dict['main']:
            box_show = BOX_Dict['main'][0]
        show_result(user_id, bot, user_id_token, Flag4XF, key_shown, None, *shown4customer[user_id_token], **box_show)

    else:

        temp_box4title = func_box(*shown4customer[user_id_token])
        result_title = await db4other("Product_Check",  table_name = file_name)
        Flag4XF = "F"
        if temp_box4title:
            if temp_box4title["title"] in result_title:
                Flag4XF = "X"
            
        if Input_Control == "data":
            
            if Intrance[:1] == "D":
                customer_stage[user_id_token] = "Delete"

                customer_order[user_id_token] = Intrance[1:]

                key_setting = InlineKeyboardMarkup(inline_keyboard = [
                    [dict(text='بله️', callback_data = "yes"),InlineKeyboardButton(text='خیر', callback_data = "no")]])
                try:
                    bot.editMessageText(message_id, delete_message, reply_markup = key_setting)
                except:
                    pass
                
            elif Intrance[:1] == "E":
                customer_stage[user_id_token] = "Edit"
                customer_order[user_id_token] = Intrance[1:]
                key_setting = await keymaker4pr(Intrance[1:])
                try:
                    bot.editMessageText(message_id, edit_witch_part, reply_markup = key_setting)
                except:
                    pass
                
            elif Intrance[:1] == "F":

                customer_stage[user_id_token] = "Finished"

                Box4title = await db4other("Title_check_Box_choose", title = Intrance[1:], table_name = file_name)
                
                Box4title['table_name'] = file_name

                await db4other("Product_Exists", table_name = file_name, title = Intrance[1:])

                dic4editmessage[user_id_token] = "F"

                sh4c = []
                show_edited(user_id, bot, user_id_token, message_id, "X", None, *sh4c, **Box4title)

            elif Intrance[:1] == "X":

                customer_stage[user_id_token] = "Exists"

                Box4title = await db4other("Title_check_Box_choose", title = Intrance[1:], table_name = file_name)
                await db4other("Product_finished", table_name = file_name, title = Intrance[1:])

                dic4editmessage[user_id_token] = "X"

                sh4c = []
                show_edited(user_id, bot, user_id_token, message_id, "F", None, *sh4c, **Box4title)

            elif Intrance[:3] == "PRN":# give_new_name
                try:
                    bot.editMessageText(message_id, "نام فعلی کالا: \n" + str(Intrance[3:]))
                    bot.sendMessage(user_id, give_title, reply_markup = markup_determent)
                    customer_order[user_id_token] = Intrance[3:]
                    customer_stage[user_id_token] = "give_new_name"
                except:
                    pass
            elif Intrance[:3] == "PRT":# give_new_context
                context, price_ware, currency_ware, discount, file_id = await db4other("take_ChosenFromTitle", table_name = file_name, t_in = Intrance[3:])
                if context:
                    exresult = "نام فعلی کالا: \n" + str(Intrance[3:]) + "\n\n" + "متن فعلی این کالا: \n" + context.decode('utf_8')
                else:
                    exresult = "فعلا متنی برای این کالا نداریم."
                try:
                    bot.editMessageText(message_id, exresult)
                    bot.sendMessage(user_id, give_context, reply_markup = markup_determent)
                    customer_order[user_id_token] = Intrance[3:]
                    customer_stage[user_id_token] = "give_new_context"
                except:
                    pass
            elif Intrance[:3] == "PRP":# give_new_photo
                context, price_ware, currency_ware, discount, file_id = await db4other("take_ChosenFromTitle", table_name = file_name, t_in = Intrance[3:])
                try:
                    if file_id:
                        bot.editMessageText(message_id, "عکس فعلی این کالا در بالا \n\n")
                    else:
                        bot.editMessageText(message_id, "فعلا عکسی برای این کالا نداریم")
                    bot.sendMessage(user_id, give_photo_ware, reply_markup = markup_determent)
                    customer_order[user_id_token] = Intrance[3:]
                    customer_stage[user_id_token] = "give_new_photo"
                except:
                    pass
            elif Intrance[:3] == "PRR":# give_new_price
                context, price_ware, currency_ware, discount, file_id = await db4other("take_ChosenFromTitle", table_name = file_name, t_in = Intrance[3:])
                if price_ware:
                    exresult = "نام فعلی کالا: \n" + str(Intrance[3:]) + "\n\n" + "قیمت فعلی این کالا: " + price_ware.decode('utf_8') + currency_ware.decode('utf_8')
                else:
                    exresult = "فعلا قیمتی برای این کالا تعیین نشده است"
                try:
                    bot.editMessageText(message_id, exresult)
                    bot.sendMessage(user_id, give_price_ware, reply_markup = markup_determent)
                    customer_order[user_id_token] = Intrance[3:]
                    customer_stage[user_id_token] = "give_new_price"
                except:
                    pass
            elif Intrance[:3] == "PRC":# give_new_discount
                context, price_ware, currency_ware, discount, file_id = await db4other("take_ChosenFromTitle", table_name = file_name, t_in = Intrance[3:])
                if price_ware:
                    if discount:
                        exresult = "نام فعلی کالا: \n" + str(Intrance[3:]) + "\n\n" + "درصد تخفیف فعلی این کالا: " + discount.decode('utf_8') + " درصد"
                    else:
                        exresult = "فعلا فروش این کالا بدون تخفیف است"
                    try:
                        bot.editMessageText(message_id, exresult)
                        bot.sendMessage(user_id, give_discount, reply_markup = markup_determent)
                        customer_order[user_id_token] = Intrance[3:]
                        customer_stage[user_id_token] = "give_new_discount"
                    except:
                        pass
                else:
                    try:
                        bot.editMessageText(message_id, NoPriceError)
                    except:
                        pass

            elif Intrance[:3] == "det":# determent
                titles = await db4other("Product_Check", table_name = file_name)
                inkeyBoxfromTitle = [dict(text = 'ویرایش️', callback_data = ("E"+Intrance[3:])),
                                  InlineKeyboardButton(text = 'حذف', callback_data = ("D"+Intrance[3:]))]
                if titles and Intrance[3:] in titles:
                    inkeyBoxfromTitle.append(InlineKeyboardButton(text = "موجود است", callback_data = ("F"+Intrance[3:])))
                else:
                    inkeyBoxfromTitle.append(InlineKeyboardButton(text = "اتمام", callback_data = ("X"+Intrance[3:])))
                boxresultitle = await db4other("take_BoxFromTitle", table_name = file_name, t_in = str(Intrance[3:]))
                try:
                    bot.editMessageText(message_id, boxresultitle, reply_markup = InlineKeyboardMarkup(inline_keyboard = [inkeyBoxfromTitle]))
                except:
                    pass
                

            elif Intrance == "yes":
                box4delete = {'table_name':file_name ,"title":customer_order[user_id_token]}
                await db4other("delete_box", **box4delete)
                try:
                    bot.editMessageText(message_id, message_deleted)
                except:
                    pass
                

            elif Intrance == "no":
                box4title = await db4other("Title_check_Box_choose", title = customer_order[user_id_token], table_name = file_name)
                if box4title:
                    if await db4other("Product_Check", table_name = file_name) == box4title["title"]:
                        Flag4XF = "X"
                    else:
                        Flag4XF = "F"
                    show_edited (user_id, bot, user_id_token, message_id, Flag4XF, None ,None, **box4title)
                

        elif Input_Control == "text":
            flag_check_Intrance = await common_check(Intrance, bot, user_id, user_id_token)
            if not flag_check_Intrance:
                if customer_stage[user_id_token] == "give_new_name":
                    try:
                        if Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, gnname_cancelled)
                            customer_stage[user_id_token] = None
                        elif len(Intrance) > 30:
                            bot.sendMessage(user_id, Error_title)
                        else:
                            titlesfromdb = await close_store_Funnc("check_title_repetitive" , column = "title", table_name = file_name)
                            if Intrance not in titlesfromdb:
                                await db4other("changeproductindb", table_name = file_name, goal = "title", pr = Intrance, extitle = customer_order[user_id_token])
                                bot.sendMessage(user_id, title_changed, reply_markup = markup_give_title)
                                customer_stage[user_id_token] = "title_changed"
                                del customer_order[user_id_token]
                            else:
                                bot.sendMessage(user_id, title_repetetive)
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_new_context":
                    try:
                        if Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, gncontext_cancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None
                        elif len(Intrance) > 1200:
                            bot.sendMessage(user_id, Error_context)
                        else:
                            await db4other("changeproductindb", table_name = file_name, goal = "context", pr = Intrance, extitle = customer_order[user_id_token])
                            bot.sendMessage(user_id, context_changed)
                            customer_stage[user_id_token] = "context_changed"
                            del customer_order[user_id_token]
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_new_photo" and Intrance == "انصراف":
                    try:
                        key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                        bot.sendMessage(user_id, phname_cancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                        customer_stage[user_id_token] = None
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_new_price":
                    if Intrance.isdigit():
                        try:
                            if int(Intrance) > 10000000000:
                                bot.sendMessage(user_id, Error_price)
                            else:
                                await db4other("changeproductindb", table_name = file_name, goal = "currency_ware", pr = Intrance, extitle = customer_order[user_id_token])
                                await db4other("changeproductindb", table_name = file_name, goal = "price_ware", pr = "تومان", extitle = customer_order[user_id_token])
                                bot.sendMessage(user_id, price_changed)
                                customer_stage[user_id_token] = "price_changed"
                                del customer_order[user_id_token]
                        except:
                            pass
                    elif Intrance == "انصراف":
                        try:
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, gpware_cancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None
                        except:
                            pass
                    else:
                        try:
                            bot.sendMessage(user_id, give_price_ware)
                        except:
                            pass
                elif customer_stage[user_id_token] == "give_new_discount":
                    try:
                        if Intrance.isdigit() and int(Intrance) >= 0 and int(Intrance) <= 100:
                            await db4other("changeproductindb", table_name = file_name, goal = "discount", pr = Intrance, extitle = customer_order[user_id_token])
                            bot.sendMessage(user_id, discount_changed)
                            del customer_order[user_id_token]
                        elif Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, gndiscount_cancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None
                        else:
                            bot.sendMessage(user_id, mistake_discount)
                    except:
                        pass

                elif customer_stage[user_id_token] == "Add_chosen" and len(shown4customer[user_id_token]) != 6:
                    dic_first_button[user_id_token] = None
                    dic_secound_button[user_id_token] = None
                    try:
                        if Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, AddChosenCancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None
                        elif Intrance == "کلید":
                            customer_stage[user_id_token] = "Add_key"
                            bot.sendMessage(user_id, givenewkey)
                        elif Intrance == "محصول":
                            del dic_first_button[user_id_token]
                            del dic_secound_button[user_id_token]
                            if len(shown4customer[user_id_token]) == 4:
                                dic_first_button[user_id_token] = shown4customer[user_id_token][1]

                            bot.sendMessage(user_id, give_title, reply_markup = markup_give_title)
                            owner_stage[user_id_token] = "context"
                    except:
                        pass
                elif customer_stage[user_id_token] == "Edit_chosen" and len(shown4customer[user_id_token]) != 6:
                    try:
                        if len(shown4customer[user_id_token]) == 2 and Intrance in key_Box_Dict.keys():
                            bot.sendMessage(user_id, givenewkey)
                            customer_order[user_id_token] = Intrance
                            customer_stage[user_id_token] = "givenewkey1"

                        elif len(shown4customer[user_id_token]) == 4 and Intrance in key_Box_Dict[shown4customer[user_id_token][1]]:
                            bot.sendMessage(user_id, givenewkey)
                            customer_order[user_id_token] = Intrance
                            customer_stage[user_id_token] = "givenewkey2"

                        elif Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, EditChosenCancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None

                    except:
                        pass

                elif customer_stage[user_id_token] == "Delete_chosen" and len(shown4customer[user_id_token]) != 6:
                    try:
                        if Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, DeleteChosenCancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None

                        elif Intrance in key_Box_Dict.keys() and len(shown4customer[user_id_token]) == 2:
                            await db4other("delete1key", first_button = Intrance, table_name = file_name)
                            BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, keydeleted, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))

                        elif Intrance in key_Box_Dict[shown4customer[user_id_token][1]] and len(shown4customer[user_id_token]) == 4:
                            
                            await db4other("delete2key", secound_button = Intrance, table_name = file_name)
                            BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, keydeleted, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                    except:
                        pass
                elif customer_stage[user_id_token] == "givenewkey1":
                    keylimitationvar = await keylimitationfunc(Intrance)
                    if keylimitationvar == "ok":
                        try:
                            customer_stage[user_id_token] = "keychanged"
                            await db4other("edit1key", new_key = Intrance, ex_key = customer_order[user_id_token], table_name = file_name)
                            BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, keyedited, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown))
                        except:
                            pass
                    elif Intrance == "/start" or Intrance == "خروج":
                        del customer_stage[user_id_token]
                        await setting_stage(user_id, token, Intrance, Input_Control, bot, file_name, message_id)

                    elif keylimitationvar == "longer":
                        try:
                            bot.sendMessage(user_id, keyislonger)
                        except:
                            pass
                elif customer_stage[user_id_token] == "givenewkey2":
                    keylimitationvar = await keylimitationfunc(Intrance)
                    if keylimitationvar == "ok":
                        try:
                            customer_stage[user_id_token] = "keychanged"
                            await db4other("edit2key", new_key = Intrance, ex_key = customer_order[user_id_token], table_name = file_name)
                            BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, keyedited, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown))
                        except:
                            pass
                    elif Intrance == "/start" or Intrance == "خروج":
                        del customer_stage[user_id_token]
                        await setting_stage(user_id, token, Intrance, Input_Control, bot, file_name, message_id)

                    elif keylimitationvar == "longer":
                        try:
                            bot.sendMessage(user_id, keyislonger)
                        except:
                            pass
                elif customer_stage[user_id_token] == "Add_key":
                    try:
                        if Intrance == "انصراف":
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            bot.sendMessage(user_id, AddChosenCancelled, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                            customer_stage[user_id_token] = None
                        else:
                            FlagIntranceInKeys = await CheckIntranceInKeys(Intrance, *shown4customer[user_id_token])
                            if not FlagIntranceInKeys:

                                if len(shown4customer[user_id_token]) == 2:
                                    await db4other("Addnewkey", firstkey = Intrance, table_name = file_name)

                                    customer_stage[user_id_token] = "key_added"
                                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                                    key_shown[0].insert(1, KeyboardButton(text = Intrance))
                                    bot.sendMessage(user_id, Key_Added, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown))

                                elif len(shown4customer[user_id_token]) == 4:
                                    await db4other("Addnewkey2", firstkey = shown4customer[user_id_token][1],secoundkey = Intrance, table_name = file_name)

                                    customer_stage[user_id_token] = "key_added"
                                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                                    key_shown[0].insert(1, KeyboardButton(text = Intrance))
                                    bot.sendMessage(user_id, Key_Added, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown))
                            else:

                                bot.sendMessage(user_id, givenewkey)
                    except:
                        pass
                elif customer_stage[user_id_token] == "order":
                    customer_stage[user_id_token] = "End order"
                    if Intrance.isdigit():
                        co_list = ast.literal_eval(customer_order[user_id_token])
                        len_co = len(co_list)
                        result_co = []
                        for counter in range(0, len_co):
                            temp_len_co = [middle_dic[2-counter], co_list[len_co - counter - 1]]
                            result_co = temp_len_co + result_co
                        result_co[-1] = int(result_co[-1])
                        result_box = func_box(*result_co)
                        result_product4customer = title_product + result_box["title"] + "\n"
                        result_product4customer += Price_product + result_box["price_ware"] + "\n"
                        result_product4customer += number_of_product + Intrance + "\n"
                        Total_price_number = int(Intrance)*int(result_box["price_ware"])
                        result_product4customer += Total_price + str(Total_price_number) + "\n"
                        if user_id_token not in Total_price_dict:
                            Total_price_dict[user_id_token] = 0
                        Total_price_dict[user_id_token] += Total_price_number
                        result_product4customer += sum_total + str(Total_price_dict[user_id_token]) + "\n"
                        key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                        flag_order.append(user_id_token)
                        try:
                            bot.sendMessage(user_id, result_product4customer, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown))
                        except:
                            pass
                    elif Intrance == "انصراف":
                        try:
                            box4send = func_box(*shown4customer[user_id_token])
                            bot.sendMessage(user_id, BuyCancelled)
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            show_result(user_id, bot, user_id_token, Flag4XF, key_shown, *shown4customer[user_id_token], **box4send)
                            customer_stage[user_id_token] = None
                        except:
                            pass
                    else:
                        try:
                            bot.sendMessage(user_id, give_number_Of_products)
                        except:
                            pass

                elif customer_stage[user_id_token] == "characteristics":
                    try:
                        if Intrance == "درست است":
                            bot.sendMessage(user_id, wait4seller_response)
                            customer_stage[user_id_token] = "wait4seller"

                        elif Intrance == "آدرس":
                            
                            customer_stage[user_id_token] = "give_address"
                            bot.sendMessage(user_id, give_customer_address)

                        elif Intrance == "مشخصات":
                            customer_stage[user_id_token] = "give_Lname"
                            bot.sendMessage(user_id, give_customer_Lname)
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_Lname":
                    try:
                        dic_last_name[user_id_token] = Intrance
                        bot.sendMessage(user_id, give_customer_Fname)
                        customer_stage[user_id_token] = "give_Fname"
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_Fname":
                    try:
                        dic_first_name[user_id_token] = Intrance
                        bot.sendMessage(user_id, give_customer_address)
                        customer_stage[user_id_token] = "give_address"
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_address":
                    try:
                        dic_Address[user_id_token] = Intrance
                        bot.sendMessage(user_id, give_customer_Phone_Number)
                        customer_stage[user_id_token] = "give_Phone_Number"
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_Phone_Number":
                    dic_Phone_Number[user_id_token] = Intrance
                    gpn_message = yrlast_ch + "\n"
                    gpn_message += yrlast_Fname + dic_first_name[user_id_token] + "\n"
                    gpn_message += yrlast_Lname + dic_last_name[user_id_token] + "\n"
                    gpn_message += yrlast_Address + dic_Address[user_id_token] + "\n"
                    gpn_message += yrlast_Phone_Number + dic_Phone_Number[user_id_token] + "\n"
                    gpn_message += dety_n4ch + detaddnum + detnewch + "\n"
                    try:
                        bot.sendMessage(user_id, gpn_message, reply_markup = markup4ch)
                        customer_stage[user_id_token] = "characteristics"
                    except:
                        pass
                elif customer_stage[user_id_token] == "wait4seller":
                    try:
                        bot.sendMessage(user_id, wait4seller_response)
                    except:
                        pass

                elif Intrance == "بعدی":
                    flag_box4send=func_check_next(*shown4customer[user_id_token])
                    if flag_box4send:
                        shown4customer[user_id_token][-1] += 1
                        key_shown = await key_shown_func(*shown4customer[user_id_token],flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                        box4send = func_box(*shown4customer[user_id_token])
                        ex_key = None
                        titles_finished = await db4other("Product_Check", table_name = file_name)
                        Flag4XF = "X"
                        if box4send and titles_finished:
                            for first_title_finished in titles_finished[0]:
                                if box4send["title"] == first_title_finished.decode("utf-8"):
                                    Flag4XF = "F"
                        if len(shown4customer[user_id_token]) == 4:
                            ex_key = shown4customer[user_id_token][1]
                        elif len(shown4customer[user_id_token]) == 6:
                            ex_key = shown4customer[user_id_token][3] + "/" + shown4customer[user_id_token][1]
                        show_result(user_id, bot, user_id_token, Flag4XF, key_shown, ex_key, *shown4customer[user_id_token], **box4send)
                    else:
                        try:
                            bot.sendMessage(user_id, nextnotfound)
                        except:
                            pass
                elif Intrance == "ثبت":
                    if user_id_token in flag_order:
                        flag_order.remove(user_id_token)
                        if user_id_token in dic_first_name:
                            temp_statistics = yrlast_ch + "\n"
                            temp_statistics += yrlast_Fname + dic_first_name[user_id_token] + "\n"
                            temp_statistics += yrlast_Lname + dic_last_name[user_id_token] + "\n"
                            temp_statistics += yrlast_Address + dic_Address[user_id_token] + "\n"
                            temp_statistics += yrlast_Phone_Number + dic_Phone_Number[user_id_token] + "\n"
                            temp_statistics += dety_n4ch + detaddnum + detnewch
                            try:
                                bot.sendMessage(user_id, temp_statistics, reply_markup = markup4ch)
                                customer_stage[user_id_token] = "characteristics"
                            except:
                                pass
                        else:
                            customer_stage[user_id_token] = "give_Lname"
                        try:
                            bot.sendMessage(user_id, give_customer_Lname)
                        except:
                            pass
                    else:
                        try:
                            bot.sendMessage(user_id, tnxfromseller + pluskeymessage + menuskeymessage + editkeymessage)
                        except:
                            pass
                elif len(shown4customer[user_id_token]) > 2 and Intrance == "بازگشت":
                    del shown4customer[user_id_token][-3]
                    del shown4customer[user_id_token][-3]
                    shown4customer[user_id_token][-1] = 0
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                    ex_key = None
                    titles_finished = await db4other("Product_Check", table_name = file_name)
                    Flag4XF = "X"
                    if box4send and titles_finished:
                        for first_title_finished in titles_finished:
                            if box4send["title"] == first_title_finished[0].decode("utf-8"):
                                Flag4XF = "F"
                    if len(shown4customer[user_id_token]) > 2:
                        ex_key = shown4customer[user_id_token][1] 
                    show_result(user_id, bot, user_id_token, Flag4XF, key_shown, ex_key, *shown4customer[user_id_token], **box4send)

                elif len(shown4customer[user_id_token]) == 2 and (Intrance in key_Box_Dict.keys()):
                    shown4customer[user_id_token] = ["key" , Intrance , "main", 0]
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = True,flag_next = func_check_next(*shown4customer[user_id_token]))
                    titles_finished = await db4other("Product_Check", table_name = file_name)
                    Flag4XF = "X"
                    if box4send and titles_finished:
                        for first_title_finished in titles_finished:
                            if box4send["title"] == first_title_finished[0].decode("utf-8"):
                                Flag4XF = "F"
                    show_result(user_id, bot, user_id_token, Flag4XF, key_shown, Intrance, *shown4customer[user_id_token], **box4send)

                elif len(shown4customer[user_id_token]) == 4 and (Intrance in key_Box_Dict[shown4customer[user_id_token][1]]):
                    shown4customer[user_id_token][2] = "key"
                    shown4customer[user_id_token][3] = Intrance
                    shown4customer[user_id_token] += ["main", 0]
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = True,flag_next = func_check_next(*shown4customer[user_id_token]))
                    titles_finished = await db4other("Product_Check", table_name = file_name)
                    Flag4XF = "X"
                    if box4send:
                        for first_title_finished in titles_finished:
                            if box4send["title"] == first_title_finished[0].decode("utf-8"):
                                Flag4XF = "F"
                    show_result(user_id, bot, user_id_token, Flag4XF, key_shown, shown4customer[user_id_token][1] + "/" + shown4customer[user_id_token][3], *shown4customer[user_id_token], **box4send)

                else:
                    try:
                        bot.sendMessage(user_id, order_mistake)
                    except:
                        pass
