import asyncio
import telepot
import telepot.aio

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from .secound_constants import *
from .secound4show import result4show

inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [dict(text='شنبه ✅️', callback_data='شنبه'),InlineKeyboardButton(text='یکشنبه ✅', callback_data='یکشنبه')],
    [dict(text='دوشنبه ✅️', callback_data='دوشنبه'), InlineKeyboardButton(text='سه شنبه ✅️', callback_data='سه شنبه')],
    [dict(text='چهارشنبه ✅️',callback_data='چهارشنبه'), InlineKeyboardButton(text='پنجشنبه ✅', callback_data='پنجشنبه')],
    [dict(text='جمعه ✅️', callback_data='جمعه')],
    [dict(text='ثبت روز', callback_data='ثبت روز')],
    ])

markup4edition = ReplyKeyboardMarkup(keyboard=[
    [dict(text='موضوع'), KeyboardButton(text='متن محصول'), KeyboardButton(text='عکس محصول')],
    [dict(text='روزهای نمایش'), KeyboardButton(text='قیمت'), KeyboardButton(text='تخفیف')],
    [dict(text='خروج'), KeyboardButton(text='درباره رباتساز 🤖'), KeyboardButton(text='انصراف')]
    ],resize_keyboard = True)

markupnot4edition = ReplyKeyboardMarkup(keyboard=[
    [dict(text='موضوع'), KeyboardButton(text='متن محصول'), KeyboardButton(text='عکس محصول')],
    [dict(text='روزهای نمایش'), KeyboardButton(text='قیمت')],
    [dict(text='خروج'), KeyboardButton(text='درباره رباتساز 🤖'), KeyboardButton(text='انصراف')]
    ],resize_keyboard = True)

markup4noseller = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='معرفی فروشنده'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)
    
markup4seller = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='معرفی فروشنده'), KeyboardButton(text='حذف فروشنده'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

Intrance_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='نیازی نیست')] , [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

bot_setting_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖') , KeyboardButton(text='ساخت ربات'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

markup_give_title = ReplyKeyboardMarkup(keyboard=[
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

markup_give_currency_ware = ReplyKeyboardMarkup(keyboard=[
    [dict(text='ریال') , KeyboardButton(text='تومان')],
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

show_result_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='اصلاح') , KeyboardButton(text='تایید ✅')],
    [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

discount_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='تخفیف نداریم')] , [dict(text='درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)

AEcitypostkeys = ReplyKeyboardMarkup(keyboard=[
    [dict(text='ویرایش'), KeyboardButton(text='حذف'), KeyboardButton(text='افزودن')], 
    [dict(text='بازگشت'), KeyboardButton(text= 'درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ],resize_keyboard = True)
    
account_markup = ReplyKeyboardMarkup(keyboard=[
    [dict(text='حذف'), KeyboardButton(text='افزودن')], 
    [dict(text= 'درباره رباتساز 🤖'), KeyboardButton(text='خروج')],
    ], resize_keyboard = True)

def store_markup(close_control, **kwargs):
    if kwargs['user_id_token'] in seller_const4show:
        store_markup = ReplyKeyboardMarkup(keyboard=[
              [dict(text=close_control), KeyboardButton(text='تنظیمات ⚙'), KeyboardButton(text='شماره حساب')],
              [KeyboardButton(text='درباره رباتساز 🤖'), KeyboardButton(text='شارژ ربات ⛽️'), KeyboardButton(text='فروشندگان 👥'), KeyboardButton(text='پست 📬')],
              ])
    else:
        store_markup = ReplyKeyboardMarkup(keyboard=[
              [dict(text=close_control), KeyboardButton(text='تنظیمات ⚙')], 
              [dict(text='درباره رباتساز 🤖')]
              ])
    return store_markup

def common_func(Intrance, bot, user_id, token):
    user_id_token = str(user_id) + token
    if Intrance == 'بازگشت':
        if user_id_token in dic_first_button:
            del dic_first_button[user_id_token]
        if user_id_token in dic_secound_button:
            del dic_secound_button[user_id_token]
        if user_id_token in dic_context:
            del dic_context[user_id_token]
        if user_id_token in dic_title:
            del dic_title[user_id_token]
        if user_id_token in dic_currency_ware:
            del dic_currency_ware[user_id_token]
        if user_id_token in dic_unit_ware:
            del dic_unit_ware[user_id_token]
        if user_id_token in dic_price_ware:
            del dic_price_ware[user_id_token]
        if user_id_token in dic_discount:
            del dic_discount[user_id_token]
        if user_id_token in dic_photo_file:
            del dic_photo_file[user_id_token]
        if user_id_token in file_id:
            del file_id[user_id_token]

        
        if token in close_store:
            try:
                bot.sendMessage(user_id, Start_New_Bot, reply_markup=store_markup("باز کردن 🔓", user_id_token = user_id_token))
            except:
                pass
        else:
            try:
                bot.sendMessage(user_id, Start_New_Bot, reply_markup=store_markup("تعطیل 🔒", user_id_token = user_id_token))
            except:
                pass
        owner_stage[user_id_token] = "botsetting"
        return True

    elif Intrance == 'درباره رباتساز 🤖':
        return False

    else:
        return False


def test_Intrance_botsetting(Intrance, bot, user_id, token):

    if common_func(Intrance, bot, user_id, token):
       return True 
        
    elif Intrance == 'درباره رباتساز 🤖':
        try:
            bot.sendMessage(user_id, Tabligh)        
            return True
        except:
            pass
    else:
        return False
    

def test_Intrance_first_button(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 

    elif Intrance == 'ساخت ربات':
        try:
            bot.sendMessage(user_id, make_button, reply_markup=Intrance_markup)        
            return "next"
        except:
            pass
    elif Intrance == 'فروشگاه':
        if token in close_store:
            try:
                bot.sendMessage(user_id, store_setting_message, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
                return "closed_store"
            except:
                pass
        else:
            try:
                bot.sendMessage(user_id, store_setting_message, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))
                return "opened_store"
            except:
                pass


    else:

        return "None"

def test_Intrance_secound_button(Intrance, bot, user_id, token):

    if common_func(Intrance, bot, user_id, token):
       return True 
        
    elif Intrance == 'نیازی نیست':
        try:
            bot.sendMessage(user_id, give_title, reply_markup=markup_give_title)        
            return "context"
        except:
            pass
    else:
        return "None"

def test_Intrance_title(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 

    elif Intrance == 'نیازی نیست':
        try:
            bot.sendMessage(user_id, give_title, reply_markup=markup_give_title)        
            return "context"
        except:
            pass
    else:
        return "None"

def test_Intrance_context(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 

    elif len(Intrance) > 40:
        try:
            bot.sendMessage(user_id, Error_title)
            return "stay"
        except:
            pass
    elif Intrance in canotuse4title:
        try:
            bot.sendMessage(user_id, Error_title_reserved)
        except:
            pass

    else:
        return "None"

def test_Intrance_photo_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 
   
    elif Intrance == 'نیازی نیست':
        return "unit_ware"
    
    elif len(Intrance) > 1500:
        try:
            bot.sendMessage(user_id, Error_context)
        except:
            pass

    else:
        return "None"

def test_Intrance_unit_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 

    elif Intrance == 'نیازی نیست':
        return "discount"    
    
    else:
        return "None"

def test_Intrance_price_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 

    elif len(Intrance) > 30:
        try:
            bot.sendMessage(user_id, Error_unit_ware)
        except:
            pass

    else:
        return "None"

def test_Intrance_currency_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 
    
    else:
        return "None"



def test_Intrance_discount(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return 'back_start'
    elif Intrance == 'نیازی نیست':
        return "result_ware"    
    else:
        return "None"


def test_Intrance_result_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return 'back_start' 

    elif Intrance == 'تخفیف نداریم':
        return "day_showing"
    
    else:
        return "None"


def test_Intrance_day_showing(Intrance, bot, user_id, token):

    if common_func(Intrance, bot, user_id, token):
       return True 

    else:
        return "None"


def test_Intrance_next_ware(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return 'back_start' 

    elif Intrance == 'تایید ✅':
        return "next_ware"
        
    elif Intrance == "اصلاح":
        return "amendment"
    
    else:
        return "None"

def test_Intrance_day_showing(Intrance, bot, user_id, token):
    if common_func(Intrance, bot, user_id, token):
       return True 
    elif Intrance == 'ذخیره و بعدی':
        return "next_ware"    
    else:
        return "None"

def show_result_ware(Intrance, bot, user_id, user_id_token):
    try:
        bot.sendMessage(user_id, give_result_ware,reply_markup= show_result_markup)
        if user_id_token in dic_first_button and dic_first_button[user_id_token]:
            bot.sendMessage(user_id, result12)
            if user_id_token in dic_secound_button and dic_secound_button[user_id_token]:
                try:
                    bot.sendMessage(user_id, dic_first_button[user_id_token] + "/" + dic_secound_button[user_id_token])
                except:
                    pass
            else:
                try:
                    bot.sendMessage(user_id, dic_first_button[user_id_token])
                except:
                    pass
                    
        if user_id_token not in dic_photo_file:
            dic_photo_file[user_id_token] = None
        if user_id_token not in dic_context:
            dic_context[user_id_token] = None
        if user_id_token not in dic_discount:
            dic_discount[user_id_token] = None
        if user_id_token not in dic_currency_ware:
            dic_currency_ware[user_id_token] = None
        if user_id_token not in file_id:
            file_id[user_id_token] = None
        if user_id_token not in dic_price_ware:
            dic_price_ware[user_id_token] = None
        if user_id_token not in dic_unit_ware:
            dic_unit_ware[user_id_token] = None

        result4show(user_id, bot, user_id_token,
                    show_title = dic_title[user_id_token],
                    show_photo_file = file_id[user_id_token],
                    show_context = dic_context[user_id_token],
                    show_discount = dic_discount[user_id_token],
                    show_currency_ware = dic_currency_ware[user_id_token],
                    show_price_ware = dic_price_ware[user_id_token],
                    show_unit_ware = dic_unit_ware[user_id_token])
    except:
        pass
    
async def making_inline_buttons(*args):
    Days_List = ['شنبه', 'یکشنبه', "دوشنبه", "سه شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
    counter4inline_markup = 0
    my_inline_keyboard = []
    temp_inline_keyboard = []
    for my_day in Days_List:
        counter4inline_markup += 1
        if my_day in args:
            day_choose = ' ✅️'
        else:
            day_choose = ' ❌'
        if counter4inline_markup % 2 != 0:
            temp_inline_keyboard.append(dict(text = (my_day + " " + day_choose) , callback_data = my_day))
        else:
            temp_inline_keyboard.append(InlineKeyboardButton(text = (my_day + " " + day_choose) , callback_data = my_day))
            my_inline_keyboard.append(temp_inline_keyboard)
            temp_inline_keyboard = []
            
    else:
        my_inline_keyboard.append(temp_inline_keyboard)
        temp_inline_keyboard = []
        temp_inline_keyboard.append(dict(text = 'ثبت روز', callback_data = 'ثبت روز'))
        my_inline_keyboard.append(temp_inline_keyboard)
    return my_inline_keyboard


def test_Intrance_closed_store(Intrance, bot, user_id):
    if Intrance == '/start' or Intrance == 'بازگشت':
        try:
            bot.sendMessage(user_id, Start_New_Bot, reply_markup=markup)
            return "back"
        except:
            pass
    elif Intrance == 'راهنمایی':
        try:
            bot.sendMessage(user_id, robot_presentation + robot_presentation2 + robot_presentation3, reply_markup=markup)
            return "stay"
        except:
            pass
    elif Intrance == 'پشتیبانی':
        try:
            bot.sendMessage(user_id, robot_presentation2)        
            return "stay"
        except:
            pass
    elif Intrance == 'باز کردن 🔓':
        try:
            bot.sendMessage(user_id, store_is_open, reply_markup = store_markup("تعطیل 🔒", user_id_token = user_id_token))
            return "open_store"
        except:
            pass
    elif Intrance == 'محصولات':
        try:
            bot.sendMessage(user_id, make_button, reply_markup=Intrance_markup)        
        except:
            pass

        return "Products"

    else:
        return "None"
    

def test_Intrance_opened_store(Intrance, bot, user_id):

    if Intrance == '/start' or Intrance == 'بازگشت':
        try:
            bot.sendMessage(user_id, Start_New_Bot, reply_markup=markup)
            return "back"
        except:
            pass

        
    elif Intrance == 'راهنمایی':
        try:
            bot.sendMessage(user_id, robot_presentation + robot_presentation2 + robot_presentation3, reply_markup=markup)
            return "stay"                                       
        except:
            pass
    elif Intrance == 'پشتیبانی':
        try:
            bot.sendMessage(user_id, robot_presentation2)        
            return "stay"
        except:
            pass
    elif Intrance == 'تعطیل 🔒':
        try:
            bot.sendMessage(user_id, store_is_closed, reply_markup = store_markup("باز کردن 🔓", user_id_token = user_id_token))
            return "close_store"
        except:
            pass
    elif Intrance == 'محصولات':
        try:
            bot.sendMessage(user_id, make_button, reply_markup=Intrance_markup)        
            return "Products"
        except:
            pass

    else:
        return "None"
