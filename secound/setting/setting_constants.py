BOX_Dict = {}
key_Box_Dict = {}
customer_stage = {}
flag_Test_file_name = []
file_name_BOX_Dict = {}
Complete_Order = []
customer_order = {}
dic_user_id = {}
dic_user_name = {}
dic_first_name = {}
dic_last_name = {}
dic_Address = {}
dic_Phone_Number = {}
shown4customer = {}
Total_price_dict = {}
dic4editmessage = {}
flag_order = []
new_key_dict = {}
give_ch = []
give_Add = []

middle_dic = ["key", "key", "main"]
delete_message = "آیا نسبت به حذف این محصول مطمئن هستید؟ ⁉️"
message_deleted = "این محصول از پایگاه داده حذف شد. ❌"
give_number_Of_products = "لطفا تعداد سفارش خود را بنویسید."
BuyCancelled = "سفارش این کالا لغو شد. ❌"
tnxfromseller = "🙏  از این که این رباتساز را برای ساخت فروشگاه خود انتخاب کردید، صمیمانه سپاسگزاریم. \n\n"
pluskeymessage = "😉 کلید « + » که معلومه چیکار می کنه! کلید و یا محصول رو برات درست می کنه. \n\n"
menuskeymessage = "⛔️ کلید « - » برای اینه که کلیدی رو که قبلا درست کرده ای، بتونی حذف کنی. \n\n"
editkeymessage = "📝 اگه می خوای کلیدی رو که قبلا درست کرده ای ویرایش کنی، کلید ویرایش هست. \n\n"
newproductkey = "هر جا کلید «محصول جدید» دیدی تعجب نکن. 😳 اونجا دیگه نمی تونی کلید جدید بسازی، فقط می تونی محصول جدید بسازی. (باور نداری امتحان کن.) برای همین بجای کلید « + » ، کلید «محصول جدید» هست. \n\n"
next_product = "کالا/مطلب بعدی"
order_mistake = "خطا در ورود اطلاعات."
nextnotfound = "متاسفانه کالای بعدی وجود ندارد. 😔"

yrlast_ch = "مشخصات قبلی شما به صورت زیر است:"
yrlast_Fname = "نام: "
yrlast_Lname = "نام خانوادگی: "
yrlast_Address = "آدرس: "
yrlast_Phone_Number = "شماره تماس: "
dety_n4ch = " چنانچه این مشخصات درست است، گزینه «درست است» رابزنید. 👌\n"
detaddnum = "چنانچه می خواهید سفارشات شما به آدرس دیگری ارسال شود، گزینه «آدرس» را فشار دهید. 📬\n"
detnewch = "چنانچه می خواهید کلیه مشخصات خود را تغییر دهید، بر روی گزینه «مشخصات» کلیک کنید. 🚶"
Key_Added = "کلید جدید اضافه شد. 👌"
Price_product = "قیمت محصول: "
title_product = "نام محصول: "
number_of_product = "تعداد: "
Total_price = "قیمت کل: "
sum_total = "جمع کل: "

give_customer_address = "لطفا  آدرس خود را بنویسید 📬 . "
give_customer_Phone_Number = "لطفا شماره موبایل خود را وارد کنید 📱 : "
wait4seller_response = "لطفا کمی صبر کنید تا سفارشات شما برای فروشنده ارسال، و نتیجه را به شما اعلام کنم. ⏳"

give_customer_Fname = "لطفا نام خود را بنویسید."
give_customer_Lname = "لطفا نام خانوادگی خود را بنویسید."

chosekeyorbox = "می خواهید کلید اضافه شود 🔑 و یا محصول 🍴 ؟"
Editkey = " لطفا کلیدی که می خواهید تغییر دهید را فشار دهید 🔑"
deletekey = "لطفا کلیدی که می خواهید حذف شود را فشار دهید 🔑"

givenewkey = "لطفا نام کلید جدید را بنویسید🔑 . "
AddChosenCancelled = "کلید اضافه نشد. 😔"
DeleteChosenCancelled = "کلیدی حذف نشد. 😔"
EditChosenCancelled = "کلیدی ویرایش نشد. 😔"
phexist_cancelled = "این کالا عکس ندارد. اگه هم داشت، حذف شد. 🤓"
keyedited = "نام کلید با موفقیت تغییر کرد. 😉"
keydeleted = "کلید با موفقیت حذف شد 😉 \n . کلید بعدی را برای حذف کردن انتخاب کنید. در غیر اینصورت کلید «خروج» یا «انصراف» را بزنید."

title_changed = "نام کالا با موفقیت تغییر یافت 👌"
price_changed = "قیمت این کالا با موفقیت تغییر کرد. 👌"
discount_changed = "درصد تخفیف این کالا با موفقیت تغییر یافت. 👌"
gnname_cancelled = "نام کالا تغییر نکرد. 😊"
edit_witch_part = "کدام قسمت را می خواهید تغییر دهید؟"
context_changed = "متن مربوط به این کالا با موفقیت تغییر کرد."
context_not_exists = 'متنی در رابطه با این موضوع وجود ندارد. 🤓'
file_id_changed = "عکس مربوط به این کالا با موفقیت تغییر کرد. 👌"
phname_cancelled = "عکس کالا تغییر نکرد. 😊"
gncontext_cancelled = " متن مربوط به توضیحات این کالا تغییر نکرد. 😊"
gpware_cancelled = "قیمت جنس ثابت ماند. 😊"
no_price_existed = "قیمت ندادید، اگه قیمت هم داده بودید حذف شد."    
Error_title = "نام کالا به درستی انتخاب نشده است"
NoPriceError = "وقتی برای کالا قیمتی نگذاشته ایم، عملا تخفیف هم نمی تونیم داشته باشیم که؟!!!"

