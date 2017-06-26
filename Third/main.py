import ast
import asyncio
import datetime
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .Third_constants import *
from .third4show import show_result
from .db_others import db4other
from ..secound.secound_constants import *
from ..first.db_takjoy import db4takjoy

markup4ch = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درست است') , KeyboardButton(text='آدرس'), KeyboardButton(text='مشخصات')],
    [dict(text='راهنمایی') , KeyboardButton(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ], resize_keyboard = True)

markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='تنظیمات')]
    ],resize_keyboard = True)

def func_inline4acceptationseller(Customer_Key):
    return InlineKeyboardMarkup(inline_keyboard = [[dict(text = 'رد شود', callback_data = "CustomerN" + Customer_Key),
                                                    InlineKeyboardButton(text = 'تایید شود', callback_data = ("CustomerY"+ Customer_Key))]])
def func_photo_payment_acceptation(Customer_Key):
    return InlineKeyboardMarkup(inline_keyboard = [[dict(text = 'تایید نهایی', callback_data = "CustomerFinalok" + Customer_Key)],
                                                   [dict(text = 'مورد تایید نیست.', callback_data = ("CustomerFinalrefused"+ Customer_Key))]])

async def make_button(flag_back = False, flag_next = False, *args, **kwargs):
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

        markup_in.append(KeyboardButton(text = 'درباره رباتساز 🤖'))
        if "user_id_token" in kwargs and kwargs["user_id_token"] in all_orthers_dict:
            markup_in.append(KeyboardButton(text = "لغو سفارش"))
            if kwargs["user_id_token"] not in saving_flag:
                markup_in.append(KeyboardButton(text = "ثبت"))

        if flag_next:
            markup_in.append(KeyboardButton(text = "بعدی"))
        markup_in.append(KeyboardButton(text = "خروج"))
        temp_markup.append(markup_in)

    return temp_markup

async def exit_from_order(user_id, token, bot, file_name, **kwargs):
    user_id_token = str(user_id) + token
    if user_id_token in Total_price_dict:
        del Total_price_dict[user_id_token]
    if user_id_token in all_orthers_dict:
        del all_orthers_dict[user_id_token]
    if user_id_token in final_gpn:
        del final_gpn[user_id_token]
    if user_id_token in customer_stage:
        del customer_stage[user_id_token]
    if user_id_token in customer_order:
        del customer_order[user_id_token]
    if user_id_token in shown4customer:
        del shown4customer[user_id_token]
    if user_id_token in purchase_citypost:
        del purchase_citypost[user_id_token]
    if user_id_token in citytaked:
        citytaked.remove(user_id_token)
    if user_id_token in flag4mine:
        flag4mine.remove(user_id_token)

    await third_stage(user_id, token, " ", "text", bot, file_name, **kwargs)

async def third_stage(user_id, token, Intrance, Input_Control, bot, file_name, **kwargs):
    user_id_token = str(user_id) + token
    BOX_Dict, key_Box_Dict = await db4other("db2mem_BOX", table_name = file_name)

    async def common_check(Intrance, bot, chat_id):
        if Intrance == '/start' or Intrance == 'خروج':
            if user_id_token in Total_price_dict:
                del Total_price_dict[user_id_token]
            if user_id_token in all_orthers_dict:
                del all_orthers_dict[user_id_token]
            if user_id_token in citytaked:
                citytaked.remove(user_id_token)
            if user_id_token in final_gpn:
                del final_gpn[user_id_token]
            if user_id_token in customer_stage:
                del customer_stage[user_id_token]
            if user_id_token in customer_order:
                del customer_order[user_id_token]
            if user_id_token in shown4customer:
                del shown4customer[user_id_token]
            if user_id_token in flag_order:
                flag_order.remove(user_id_token)
            key_shown = await make_button(2, False,bool(len(BOX_Dict['main']) > 1),*list(key_Box_Dict.keys()))
            if user_id_token in saving_flag:
                try:
                    bot.sendMessage(chat_id, order_cancelled, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                    saving_flag.remove(user_id_token)
                except:
                    pass
            owner_stage[user_id_token] = "botsetting"
            if user_id_token in shown4customer:
                del shown4customer[user_id_token]
            return True
        elif Intrance == 'درباره رباتساز 🤖':
            try:
                bot.sendMessage(chat_id, Tabligh)
            except:
                pass
            return True
        elif user_id_token in all_orthers_dict and Intrance == "لغو سفارش":
            del all_orthers_dict[user_id_token]
            if user_id_token in saving_flag:
                saving_flag.remove(user_id_token)
            if user_id_token in shown4customer:
                del shown4customer[user_id_token]
            if user_id_token in Total_price_dict:
                del Total_price_dict[user_id_token]
            try:
                bot.sendMessage(chat_id, BuyCancelled)
            except:
                pass
            shown4customer[user_id_token] = ["main" , 0]
            key_shown = await make_button(False,bool(len(BOX_Dict['main']) > 1),*list(key_Box_Dict.keys()), user_id_token = user_id_token)
            customer_stage[user_id_token] = "first"
            box_show = BOX_Dict['main'][0]
            await show_result(user_id, bot, user_id_token, key_shown, None, *shown4customer[user_id_token], File_name = file_name , **box_show)
            return True
        else:
            return False

    def func_box(*args):
        temp4calc = BOX_Dict
        flag_temp4calc = True
        for i in range(0, len(args)-1):
            temp_in = temp4calc[args[i]]
            temp4calc = temp_in
        if args[-1] < len(temp4calc):
            return temp4calc[args[-1]]
        else:
            return False

    async def key_shown_func(*args,flag_back = False, flag_next = False):

        temp_key_shown = list(args)
        if len(temp_key_shown) == 2:

            key_shown = await make_button(False, flag_next, *list(key_Box_Dict.keys()), user_id_token = user_id_token)
        elif len(temp_key_shown) == 4:

            key_shown = await make_button(True, flag_next, *key_Box_Dict[temp_key_shown[1]], user_id_token = user_id_token)
        elif len(temp_key_shown) == 6:

            key_shown = await make_button(True, flag_next, user_id_token = user_id_token)
        return key_shown

    def func_check_next(*args):
        temp = list(args)
        temp[-1] += 1
        box4next = func_box(*temp)
        if box4next:
            return True
        else:
            return False

    flag_check_Intrance = False
    flag_check_Intrance = await common_check(Intrance, bot, user_id)
    if user_id_token not in shown4customer:
        shown4customer[user_id_token] = ["main" , 0]
        key_shown = await make_button(False,bool(len(BOX_Dict['main']) > 1),*list(key_Box_Dict.keys()), user_id_token = user_id_token)
        customer_stage[user_id_token] = "first"
        box_show = BOX_Dict['main'][0]
        await show_result(user_id, bot, user_id_token, key_shown, None, *shown4customer[user_id_token], File_name = file_name, **box_show)

    else:
        if Input_Control == "data":
            try:
                if Intrance[:12] == "bill_payment":
                    inline4payment_photo = InlineKeyboardMarkup(inline_keyboard = [[dict(text = 'عکس فیش آماده نیست', callback_data = "take_photo" + Intrance[12:])]])
                    customer_char_temp[user_id_token] = Intrance[12:]
                    bot.editMessageText(kwargs['message_id'], give_your_payment_photo, reply_markup = inline4payment_photo)
                    customer_stage[user_id_token] = "take_photo_of_order"
                elif Intrance[:12] == "bill_cancel0":
                    bot.editMessageText(kwargs['message_id'], order_cancelled)
                    await exit_from_order(user_id, token, bot, file_name, **kwargs)
                elif user_id_token in customer_stage and customer_stage[user_id_token] == "take_photo_of_order":
                    inline_markup4bill_payment = InlineKeyboardMarkup(inline_keyboard = [[dict(text='ارسال فیش', callback_data = "bill_payment" + Intrance[1:])],
                                                                             [dict(text='انصراف', callback_data = "bill_cancel0" + Intrance[1:])]])
                    result_all_account = await db4takjoy('account_db', ctrl_account = "take_all_from_db", table_num = file_name)
                    if user_id_token in purchase_citypost:
                        message2customer = ''
                        for accounts in result_all_account:
                            message2customer += accounts[0].decode('utf8') + ' به نام: ' + accounts[1].decode('utf8') + "\n"
                    bot.editMessageText(kwargs['message_id'], pay_price.format(price = str(int(Total_price_dict[user_id_token]) + int(purchase_citypost[user_id_token]))) +
                    "\n\n" + message2customer + "\n 🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻 \n" + pay_attention_pay_price, reply_markup = inline_markup4bill_payment)

                elif user_id_token not in saving_flag:
                    key_setting = await make_button(None, None, "انصراف", user_id_token = user_id_token)
                    bot.sendMessage(user_id, give_number_Of_products, reply_markup = ReplyKeyboardMarkup(keyboard = key_setting, resize_keyboard = True))
                    customer_stage[user_id_token] = "order"
                    customer_order[user_id_token] = Intrance
                else:
                    bot.sendMessage(user_id, mistake4give_order)
            except:
                pass
        elif Input_Control == "photo" and user_id_token in customer_stage and customer_stage[user_id_token] == "take_photo_of_order":
            saving_flag.remove(user_id_token)
            photo_file = bot.getFile(Intrance)
            for seller_list in (seller_dict[user_id4owner[token]]):
                try:
                    bot.sendPhoto(seller_list[0], photo_file["file_id"])
                    bot.sendMessage(seller_list[0], customer_order_characteristic[customer_char_temp[user_id_token]])
                except:
                    pass
            del customer_char_temp[user_id_token]
            bot.sendMessage(user_id, order_photo_sent2seller)
            await exit_from_order(user_id, token, bot, file_name, **kwargs)

        if Input_Control == "text":
            if not flag_check_Intrance:
                if customer_stage[user_id_token] == "order":
                    try:
                        if Intrance.isdigit():
                            if user_id_token not in all_orthers_dict:
                                all_orthers_dict[user_id_token] = []
                            price, discount = await db4other("give_price_from_title4customer", table_name = str(file_name), title_of_product = customer_order[user_id_token])
                            if discount:
                                result_price = ((100 - int(discount))*int(price))/100
                            else:
                                result_price = price
                            all_orthers_dict[user_id_token].append([customer_order[user_id_token], Intrance, result_price])
                            result_product4customer = Price_product + str(int(result_price)) + "تومان" + "\n"
                            result_product4customer += number_of_product + Intrance + "\n"
                            Total_price_number = int(Intrance)*int(result_price)
                            result_product4customer += Total_price + str(Total_price_number) + "تومان" + "\n"
                            if user_id_token not in Total_price_dict:
                                Total_price_dict[user_id_token] = 0
                            Total_price_dict[user_id_token] += Total_price_number
                            result_product4customer += sum_total + str(Total_price_dict[user_id_token]) + "تومان" + "\n"
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            flag_order.append(user_id_token)
                            try:
                                bot.sendMessage(user_id, result_product4customer, reply_markup = ReplyKeyboardMarkup(keyboard=key_shown, resize_keyboard = True))
                            except:
                                pass

                        elif Intrance == "انصراف":
                            box4send = func_box(*shown4customer[user_id_token])
                            key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                            try:
                                bot.sendMessage(user_id, BuyCancelled, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                            except:
                                pass

                        else:
                            try:
                                bot.sendMessage(user_id, give_number_Of_products)
                            except:
                                pass
                        customer_stage[user_id_token] = "End order"
                    except:
                        pass
                elif customer_stage[user_id_token] == "characteristics":
                    if Intrance == "درست است":

                        if user_id_token in saving_flag and user_id_token not in city_dict:
                            saving_flag.remove(user_id_token)
                        now = datetime.datetime.now()
                        customer_char = now.year + now.month + now.day + now.hour + now.minute + now.second
                        try:
                            bot.sendMessage(user_id, wait4seller_response)
                        except:
                            pass
                        if user_id_token in flag4mine:
                            flag4mine.remove(user_id_token)
                        message4customer_characteristics = ''
                        Customer_Key = str(user_id) + "C" + str(customer_char)
                        for customer_characteristics in all_orthers_dict[user_id_token]:
                            message4customer_characteristics += str(customer_characteristics[0]) + "\n قیمت:" + str(customer_characteristics[2]) + "تومان \n\n تعداد:" + str(customer_characteristics[1]) + "\n" + 2 * " 🌺🌻🌹 🌼🌷🌸 " + "\n"
                        customer_order_characteristic[Customer_Key] = message4customer_characteristics + "\n" + final_gpn[user_id_token]
                        for seller_list in (seller_dict[user_id4owner[token]]):
                            if seller_list[0]:
                                try:
                                    bot.sendMessage(seller_list[0], customer_order_characteristic[Customer_Key], reply_markup = func_inline4acceptationseller(Customer_Key))
                                except:
                                    pass
                            else:
                                try:
                                    bot.sendMessage(int(user_id4owner[token][:-len(token)]), seller_not_endorsed.format(seller = seller_list[1]))
                                    bot.sendMessage(int(user_id4owner[token][:-len(token)]), customer_order_characteristic[Customer_Key], reply_markup = func_inline4acceptationseller(Customer_Key))
                                except:
                                    pass
                        del customer_stage[user_id_token]

                    elif Intrance == "آدرس":
                        try:
                            bot.sendMessage(user_id, give_customer_address)
                            customer_stage[user_id_token] = "give_address"
                        except:
                            pass
                    elif Intrance == "مشخصات":
                        try:
                            bot.sendMessage(user_id, give_customer_Lname)
                            customer_stage[user_id_token] = "give_Lname"
                        except:
                            pass
                elif customer_stage[user_id_token] == "give_Lname":
                    try:
                        bot.sendMessage(user_id, give_customer_Fname)
                        customer_stage[user_id_token] = "give_Fname"
                        dic_last_name[user_id_token] = Intrance
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_Fname":
                    try:
                        if file_name in dict_citypost and dict_citypost[file_name] and user_id_token not in citytaked:
                            Temp_citypost_list = []
                            for Temp_citypost in dict_citypost[file_name]:
                                Temp_citypost_list.append(Temp_citypost[0])
                            key4city = await make_button(False, False, *Temp_citypost_list)
                            bot.sendMessage(user_id, give_customer_city, reply_markup = ReplyKeyboardMarkup(keyboard = key4city, resize_keyboard = True))
                            customer_stage[user_id_token] = "give_city"
                            citytaked.append(user_id_token)
                        else:
                            if user_id_token in citytaked:
                                citytaked.remove(user_id_token)
                            bot.sendMessage(user_id, give_customer_address)
                            customer_stage[user_id_token] = "give_address"
                        dic_first_name[user_id_token] = Intrance
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_address":
                    key_shown = await key_shown_func(*shown4customer[user_id_token])
                    dic_Address[user_id_token] = Intrance
                    try:
                        if user_id_token in purchase_citypost:
                            customer_stage[user_id_token] = "give_postal_code"
                            bot.sendMessage(user_id, give_postal_code, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                        else:
                            bot.sendMessage(user_id, give_customer_Phone_Number, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                            customer_stage[user_id_token] = "give_Phone_Number"
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_postal_code":
                    try:
                        if Intrance.isdigit() and len(Intrance) == 10:
                            await db4other('postal_code2db', table_name = file_name)
                            bot.sendMessage(user_id, give_customer_Phone_Number)
                            postal_code[user_id_token] = Intrance
                            customer_stage[user_id_token] = "give_Phone_Number"
                        else:
                            bot.sendMessage(user_id, give_postal_code)
                    except:
                        pass
                elif customer_stage[user_id_token] == "give_city":
                    citytaked.remove(user_id_token)
                    for citybox in dict_citypost[file_name]:
                        if Intrance == citybox[0]:
                            purchase_citypost[user_id_token] = citybox[1]
                            customer_stage[user_id_token] = "give_address"
                            city_dict[user_id_token] = Intrance
                            key_shown = await key_shown_func(*shown4customer[user_id_token])
                            try:
                                bot.sendMessage(user_id, post_purchase_added.format(purchase = str(citybox[1]), Total_Price = str(int(citybox[1])+int(Total_price_dict[user_id_token]))) + "\n" + give_customer_address, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                            except:
                                pass
                            Total_price_dict[user_id_token] = str(int(citybox[1])+int(Total_price_dict[user_id_token]))
                            break
                    else:
                        try:
                            bot.sendMessage(user_id, give_customer_city)
                        except:
                            pass

                elif customer_stage[user_id_token] == "give_Phone_Number":
                    if Intrance.isdigit() or (Intrance[1:].isdigit() and Intrance[0] == "+"):
                        dic_Phone_Number[user_id_token] = Intrance
                        gpn_message = yrlast_ch + "\n"
                        gpn_message += yrlast_Fname + dic_first_name[user_id_token] + "\n"
                        gpn_message += yrlast_Lname + dic_last_name[user_id_token] + "\n"
                        if user_id_token in city_dict:
                            gpn_message += yrlast_Cityname + city_dict[user_id_token] + "\n"
                        gpn_message += yrlast_Address + dic_Address[user_id_token] + "\n"
                        if user_id_token in postal_code:
                            gpn_message += yrlast_PostalCode + postal_code[user_id_token] + "\n"
                        gpn_message += yrlast_Phone_Number + dic_Phone_Number[user_id_token] + "\n"
                        Help4final_key_customer = dety_n4ch + detaddnum + detnewch + "\n"
                        message4customer_characteristics = ""
                        for customer_characteristics in all_orthers_dict[user_id_token]:
                            message4customer_characteristics += str(customer_characteristics[0]) + "\n قیمت:" + str(customer_characteristics[2]) + "تومان \n\n تعداد:" + str(customer_characteristics[1]) + "\n" + 2 * " 🌺🌻🌹 🌼🌷🌸 " + "\n"
                        try:
                            bot.sendMessage(user_id, message4customer_characteristics + "قیمت نهایی:" + str(Total_price_dict[user_id_token]) + "\n" + gpn_message + Help4final_key_customer, reply_markup = markup4ch)
                        except:
                            pass
                        final_gpn[user_id_token] = gpn_message
                        customer_stage[user_id_token] = "characteristics"
                        await db4other("mem2db_customer", table_name = file_name, key_acc = user_id_token)
                    else:
                        try:
                            bot.sendMessage(user_id, give_customer_Phone_Number, reply_markup = ReplyKeyboardMarkup(keyboard = key_shown, resize_keyboard = True))
                        except:
                            pass

                elif Intrance == "بعدی":
                    flag_box4send=func_check_next(*shown4customer[user_id_token])
                    if flag_box4send:
                        shown4customer[user_id_token][-1] += 1
                        key_shown = await key_shown_func(*shown4customer[user_id_token],flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                        box4send = func_box(*shown4customer[user_id_token])
                        ex_key = None
                        titles_finished = await db4other("Title_Check", table_name = file_name)
                        Flag4XF = "X"

                        if box4send and titles_finished:
                            for title_finished in titles_finished[0]:
                                if box4send["title"] in title_finished.decode("utf-8"):
                                    Flag4XF = "F"
                        if len(shown4customer[user_id_token]) == 4:
                            ex_key = shown4customer[user_id_token][1]
                        elif len(shown4customer[user_id_token]) == 6:
                            ex_key = shown4customer[user_id_token][3] + "/" + shown4customer[user_id_token][1]
                        await show_result(user_id, bot, user_id_token, key_shown, ex_key, *shown4customer[user_id_token], File_name = file_name, **box4send)
                    else:
                        try:
                            bot.sendMessage(user_id, nextnotfound)
                        except:
                            pass


                elif Intrance == "ثبت":
                    saving_flag.append(user_id_token)
                    markup4saving = await make_button(False, False, user_id_token = user_id_token)

                    if user_id_token in flag_order:
                        flag_order.remove(user_id_token)

                        if user_id_token in dic_first_name:
                            if user_id_token in city_dict:
                                for citybox in dict_citypost[file_name]:
                                    if city_dict[user_id_token] == citybox[0]:
                                        try:
                                            bot.sendMessage(user_id, message4customer_city.format(city_name = citybox[0], city_purchase = str(citybox[1])))
                                        except:
                                            pass
                                        Total_price_dict[user_id_token] = str(int(Total_price_dict[user_id_token]) + int(citybox[1]))
                            temp_statistics = yrlast_ch + "\n"
                            temp_statistics += yrlast_Fname + dic_first_name[user_id_token] + "\n"
                            temp_statistics += yrlast_Lname + dic_last_name[user_id_token] + "\n"
                            if user_id_token in city_dict:
                                temp_statistics += yrlast_Cityname + city_dict[user_id_token] + "\n"
                            temp_statistics += yrlast_Address + dic_Address[user_id_token] + "\n"
                            if user_id_token in postal_code:
                                temp_statistics += yrlast_PostalCode + postal_code[user_id_token] + "\n"
                            temp_statistics += yrlast_Phone_Number + dic_Phone_Number[user_id_token] + "\n"
                            temp_key_customer = dety_n4ch + detaddnum + detnewch + detcancelled
                            message4customer_characteristics = ""
                            for customer_characteristics in all_orthers_dict[user_id_token]:
                                message4customer_characteristics += str(customer_characteristics[0]) + "\n قیمت:" + str(customer_characteristics[2]) + "تومان \n\n تعداد:" + str(customer_characteristics[1]) + "\n" + 2 * " 🌺🌻🌹 🌼🌷🌸 " + "\n"
                            try:
                                bot.sendMessage(user_id, message4customer_characteristics + "قیمت نهایی:" + str(Total_price_dict[user_id_token]) + "\n" + temp_statistics + temp_key_customer, reply_markup = markup4ch)
                                final_gpn[user_id_token] = temp_statistics
                                customer_stage[user_id_token] = "characteristics"
                            except:
                                pass
                        else:
                            try:
                                bot.sendMessage(user_id, give_customer_Lname, reply_markup = ReplyKeyboardMarkup(keyboard = markup4saving, resize_keyboard = True))
                                customer_stage[user_id_token] = "give_Lname"
                            except:
                                pass
                    else:
                        try:
                            bot.sendMessage(user_id, order_mistake)
                        except:
                            pass

                elif customer_stage[user_id_token] == "take_photo_of_order":
                    if Intrance == "انصراف":
                        await common_check("خروج", bot, chat_id)
                    else:
                        try:
                            bot.sendMessage(user_id, order_specification)
                        except:
                            pass

                elif len(shown4customer[user_id_token]) > 2 and Intrance == "بازگشت":
                    del shown4customer[user_id_token][-3]
                    del shown4customer[user_id_token][-3]
                    shown4customer[user_id_token][-1] = 0
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = bool(len(shown4customer[user_id_token]) > 2),flag_next = func_check_next(*shown4customer[user_id_token]))
                    await show_result(user_id, bot, user_id_token, key_shown, None, *shown4customer[user_id_token], File_name = file_name , **box4send)

                elif len(shown4customer[user_id_token]) == 2 and (Intrance in key_Box_Dict.keys()):
                    shown4customer[user_id_token] = ["key" , Intrance , "main", 0]
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = True,flag_next = func_check_next(*shown4customer[user_id_token]))
                    await show_result(user_id, bot, user_id_token, key_shown, Intrance, *shown4customer[user_id_token], File_name = file_name, **box4send)

                elif len(shown4customer[user_id_token]) == 4 and (Intrance in key_Box_Dict[shown4customer[user_id_token][1]]):
                    shown4customer[user_id_token][2] = "key"
                    shown4customer[user_id_token][3] = Intrance
                    shown4customer[user_id_token] += ["main", 0]
                    box4send = func_box(*shown4customer[user_id_token])
                    key_shown = await key_shown_func(*shown4customer[user_id_token], flag_back = True,flag_next = func_check_next(*shown4customer[user_id_token]))
                    await show_result(user_id, bot, user_id_token, key_shown, shown4customer[user_id_token][1] + "/" + shown4customer[user_id_token][3], *shown4customer[user_id_token], File_name = file_name , **box4send)

                else:
                    try:
                        bot.sendMessage(user_id, order_mistake)
                    except:
                        pass
