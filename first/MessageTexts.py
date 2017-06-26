loop = None
choose_file = {}
Bot_Token = {}
give_token = {}
true_token = {}
true_Bot_id = {}
saveindb = []
changeindb = []
UNT_Dict = {}
UNT_take = {}
flag_test_un = {}
impermanent_token = {}
save_new_token = {}
dic_bot_user_id = {}
dic_user_id_bot = {}
save_token = {}

witch_bot = "توکن کدام ربات را می‌خواهید تغییر دهید؟"
Welcome2urBot = "به ربات خودتون خوش اومدید. \n"
Tabligh = "رباتساز تکجوی هر روز با ایده های جدید در خدمت شما است و در جهت رضایتمندی شما عزیزان از انتقادات، پشنهادات و  از ایده های شما استقبال می کنیم." 
error_Token = "لطفاً توکن خود را درست بنویسید."
takjoy_presentation = "جهت مشاهده قالب های مختلف و راهنمایی به کانال @takjoy مراجعه فرمایید."
robot_presentation = " در این رباتساز صرفا بایستی توکن خود را معرفی نمایید. \n" 
robot_presentation2 =  """ چنانچه قبلا ربات خود را ساخته و توکن آن را در اختیار رباتساز دیگری قرار داده اید، ابتدا در @Botfather با دستور /revoke توکن خود را تغییر دهید و سپس توکن تغییر یافته را بنویسید. \n\n"""
robot_presentation3 = "جهت مشاهده نحوه ایجاد توکن و یا تغییر آن به ربات @topjoybot مراجعه فرمایید. \n"
tnx4takjoy_use = "از این که رباتساز تکجوی رو انتخاب کردید سپاسگزارم. 🙏 \n لطفا ربات {bot} را /start نمایید."
Token_not_accepted = "توکن شما معتبر نیست. لطفاً توکن معتبر بنویسید. \n"
insert_changed_Token = "لطفاً توکن جدید ربات خود را بنویسید.\n"
buttons = ["راهنمایی", "پشتیبانی", "تغییر توکن", "بازگشت", "/start", "/invoke"]
notocken4u = "شما تا کنون توسط این رباتساز رباتی نساخه اید."
mistake4username3 = "ظاهرا نسبت به ارسال درست یوزرنیم مشکل دارید. بنابراین ثبت ربات شما منتفی شد. توصیه می شود با پشتیبانی تماس گرفته و یا راهنمایی را مجددا مطالعه فرمایید."
Exists_in_DB = "این ربات قبلا ثبت شده است. در صورت بروز مشکل با پشتیبانی تماس حاصل فرمایید."
cancelled_saving_token = "ذخیره سازی ربات شما منتفی شد."
select_your_bot = "لطفاً رباتی که می خواهید توکن آن را عوض کنید را انتخاب کنید:"
cancelled_change_token = "تغییر توکن ربات شما منتفی شد."
OK_change_token = "توکن ربات شما با موفقیت تغییر یافت."
dude_make_bot = "شخصی با یوزرنیم @{u_name} ربات @{bot} را ساخت: {u_id}"
are_u_sure_ok = "مطمئنی درسته؟"
are_u_sure_no = "مطمئنی اشتباهه؟"
thirth_days_adding = '۳۰ روز اضافه شد. {day} روز تا شارژ بعدی ...'
billnotaccepted = "متاسفانه فیش شما مورد تایید قرار نگرفت. در صورت هر گونه مشکل، با @XtakjoyX تماس حاصل فرمایید."
Tokens_not_changed = "توکن تغییر نکرد."
give_new_token = "لطفا توکن جدید را وارد نمایید."
Token_is_not_correct = "توکن مربوط به این ربات نیست. لطفا توکن درست را وارد نمایید."
Guidance = "جهت راهنمایی برای نحوه ساخت ربات به @topjoybot، و جهت ارتباط با ما به @XtakjoyX مراجعه فرمایید."
Token_changed = "توکن ربات @{bot} با موفقیت تغییر یافت."
Tokens_not_changed = "توکن تغییر نکرد..."

take4test = "select Token, User_id from Token_Takjoy;"
takeToken = "select Token from Token_Takjoy;"
befor_select_all = ("""SET block_encryption_mode = 'aes-256-cbc';
              SET @key_str = SHA2('My secret passphrase',512); 
              SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';""")

select_all = ("select emp_no, AES_DECRYPT(User_id,@key_str, @init_vector), AES_DECRYPT(Token,@key_str, @init_vector), Bot_Date, AES_DECRYPT(Bot_id,@key_str, @init_vector) from Token_Takjoy;")
select4botmaker = ("select AES_DECRYPT(User_id,@key_str, @init_vector), AES_DECRYPT(Bot_id,@key_str, @init_vector) from Token_Takjoy;")
select4chargebot = ("select AES_DECRYPT(Token,@key_str, @init_vector), AES_DECRYPT(Bot_id,@key_str, @init_vector) from Token_Takjoy;")
sql = ("CREATE TABLE IF NOT EXISTS Token_Takjoy("
    "`emp_no` int(12) NOT NULL AUTO_INCREMENT,"
    "`User_id` BINARY(16) NULL,"
    "`Token` Text not NULL,"
    "`Bot_Date` datetime NULL,"
    "`Bot_ID` Text not NULL,"
    "PRIMARY KEY(emp_no));")

Update_Token = ("update Token_Takjoy set Token = AES_ENCRYPT(%s,@key_str, @init_vector) where Token = AES_ENCRYPT(%s,@key_str, @init_vector);")

Token_repeated = "این ربات قبلا ثبت شده است."
choose_your_Bot = "توکن کدامیک از ربات های خود را می خواهید عوض کنید؟"
token_changing = "ربات در حال تغییر توکن: {bot}"
