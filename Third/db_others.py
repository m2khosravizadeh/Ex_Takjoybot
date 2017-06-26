import datetime
import asyncio
import aiomysql

from .Third_constants import *
from ..secound.secound_constants import *

befor_select_all = ("""SET block_encryption_mode = 'aes-256-cbc';
              SET @key_str = SHA2('My secret passphrase',512);
              SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; """)


def TodayCanShown(num_in):
    TodayOFWeek = datetime.datetime.today().weekday()
    num = int(num_in)
    for num_day in range(0,TodayOFWeek):
        if num > num4dayList[num_day]:
            num -= num4dayList[num_day]
    else:
        if num < num4dayList[TodayOFWeek]:
            return False
        else:
            return True
        
async def db4other(flag_DB_Table, **kwargs):

    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
                              user='root', password="lk1l,tr3ldal5",charset = "utf8",
                              db='Test', loop=loop)


    cur = await conn.cursor()


    table4customer = "sec_customer_" + str(kwargs["table_name"])

    table4order = "flag4order_" + str(kwargs["table_name"])

    create_customer_table = ("CREATE TABLE IF NOT EXISTS " + table4customer + " ("
                             "`emp_nu` int(12) NOT NULL AUTO_INCREMENT,"
                             "`user_id` Text NULL,"
                             "`user_name` Text NULL,"
                             "`first_name` Text NULL,"
                             "`last_name` Text NULL,"
                             "`Address` Text NULL,"
                             "`Phone_Number` Text NULL,"
                             "`city_dict` Text NULL,"
                             "`Postal_code` Text NULL,"
                             "PRIMARY KEY(emp_nu));")
    
    give2db_city = ("""INSERT IGNORE INTO {table4customer}(city_dict) VALUES(AES_ENCRYPT({city_dict},@key_str, @init_vector) where {user_id} = user_id""")
    give2db_postal_code = ("""INSERT IGNORE INTO {table4customer}(Postal_Code) VALUES(AES_ENCRYPT({Postal_Code},@key_str, @init_vector) where {user_id} = user_id""")
    async with conn.cursor() as cur:    
        await cur.execute(create_customer_table)
        await conn.commit()
            
        if flag_DB_Table == 0:
            Daysetting = "7"
            cur = await conn.cursor()
            insert_table = ("SET block_encryption_mode = 'aes-256-cbc';"
                            "SET @key_str = SHA2('My secret passphrase',512); "
                            "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; "
                            "SET @ENCRYPT_User_id = %s; "
                            "SET @ENCRYPT_Token = %s; "
                            "INSERT IGNORE INTO Token_Takjoy(User_id, Token, Bot_Date) VALUES(AES_ENCRYPT(@ENCRYPT_User_id,@key_str, @init_vector), AES_ENCRYPT(@ENCRYPT_Token,@key_str, @init_vector), (CURDATE() + interval " + Daysetting + " day));")

            len_flag = len(saveindb)

            for i in range(0,len_flag):
                my_user_id = saveindb.pop()

                new_bot = (str(my_user_id), true_token[my_user_id])

                await cur.execute(insert_table, new_bot)
                await conn.commit()
        
        elif flag_DB_Table == "db2mem_BOX":
            table_seller_name = 'sec_sell_' + str(kwargs["table_name"])
            create_other_table = ("""CREATE TABLE IF NOT EXISTS {create_table_seller} (
                                `emp_nu` int(12) NOT NULL AUTO_INCREMENT,
                                `first_button` Text NULL,
                                `secound_button` Text NULL,
                                `title` Text NULL,
                                `context` Text NULL,
                                `price_ware` Text NULL,
                                `currency_ware` Text NULL,
                                `unit_ware` Text NULL,
                                `discount` Text NULL,
                                `photo_file` Text NULL,
                                `file_id` Text NULL,
                                `showindays` Text NULL,
                                PRIMARY KEY(emp_nu));""")
            
            select_all = ("""select `emp_nu`,
                          AES_DECRYPT(`first_button`,@key_str, @init_vector),
                          AES_DECRYPT(`secound_button`,@key_str, @init_vector),
                          AES_DECRYPT(`title`,@key_str, @init_vector),
                          AES_DECRYPT(`context`,@key_str, @init_vector),
                          AES_DECRYPT(`price_ware`,@key_str, @init_vector),
                          AES_DECRYPT(`currency_ware`,@key_str, @init_vector),
                          AES_DECRYPT(`unit_ware`,@key_str, @init_vector),
                          AES_DECRYPT(`discount`,@key_str, @init_vector),
                          AES_DECRYPT(`photo_file`,@key_str, @init_vector),
                          AES_DECRYPT(`file_id`,@key_str, @init_vector),
                          AES_DECRYPT(`showindays`,@key_str, @init_vector) from {my_table};""".format(my_table=table_seller_name))

            await cur.execute(create_other_table.format(create_table_seller = table_seller_name))
            await cur.execute(befor_select_all)
            await conn.commit()
            result_db = None
            
            await cur.execute(select_all)

            await conn.commit()

            result_db = await cur.fetchall()

            flag_Box = 0
            BOX_Temp = {}
            key_Box_Dict = {}
            BOX_Dict_Temp = {}
            BOX_Dict = {}
            BOX_Dict['key'] = {}
            BOX_Dict['main'] = []
            BOX_Dict_Temp['key'] = {}
            BOX_Dict_Temp['main'] = []
            
            for row in result_db:
                BOX_Temp = {}
                row1 = None
                row2 = None
                if row[1]:
                    row1 = row[1].decode("utf-8")

                if row[2]:
                    row2 = row[2].decode("utf-8")


                
                if row[11]:

                    if TodayCanShown(row[11]):
                
                        for i in range(3, 11):
                            if row[i]:

                                BOX_Temp[BoxList[i-3]] = row[i].decode("utf-8")
                                        
                        if not row1:
                            if BOX_Temp:
                                BOX_Dict_Temp['main'].append(BOX_Temp)
                                BOX_Temp = {}
                            
                        elif not row2:
                            if row1 not in BOX_Dict_Temp['key']:
                                BOX_Dict_Temp['key'][row1] = {}
                                BOX_Dict_Temp['key'][row1]['main'] = []
                                BOX_Dict_Temp['key'][row1]['key'] = {}
                            if BOX_Temp:
                                BOX_Dict_Temp['key'][row1]['main'].append(BOX_Temp)
                                BOX_Temp = {}

                            if row1 not in key_Box_Dict:
                                key_Box_Dict[row1] = []
                        else:

                            if row1 not in BOX_Dict_Temp['key']:
                                BOX_Dict_Temp['key'][row1] = {}
                                BOX_Dict_Temp['key'][row1]['key'] = {}
                                BOX_Dict_Temp['key'][row1]['main'] = []
                                if row1 not in key_Box_Dict:
                                    key_Box_Dict[row1] = []

                            if row2 not in BOX_Dict_Temp['key'][row1]['key']:
                                BOX_Dict_Temp['key'][row1]['key'][row2] = {}
                                BOX_Dict_Temp['key'][row1]['key'][row2]['main'] = []
                            if BOX_Temp:
                                BOX_Dict_Temp['key'][row1]['key'][row2]['main'].append(BOX_Temp)
                                BOX_Temp = {}

                            if row2 not in key_Box_Dict[row1]:
                                key_Box_Dict[row1].append(row2)

                        BOX_Dict = BOX_Dict_Temp

               
            if not BOX_Dict['main']:
                BOX_Dict['main'].append({"title":"به این فروشگاه خوش آمدید."})
            


            return BOX_Dict, key_Box_Dict

        elif flag_DB_Table == "city2db":
            await cur.execute(give2db_city.format(table4customer = table4customer))
            await conn.commit()
            
        elif flag_DB_Table == "postal_code2db":
            await cur.execute(give2db_postal_code.format(table4customer = table4customer))
            await conn.commit()

        elif flag_DB_Table == "Title_Check":

            check_order_table = ("""select AES_DECRYPT(`title`,@key_str, @init_vector) from {my_table};""".format(my_table=table4order))
            
            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(check_order_table)
            await conn.commit()
            result_db = None
            
            result_db = await cur.fetchall()
            return result_db


        elif flag_DB_Table == "db2mem_customer":

            select_special = ("select emp_nu, AES_DECRYPT(user_id,@key_str, @init_vector),"
                              "AES_DECRYPT(user_name,@key_str, @init_vector),"
                              "AES_DECRYPT(first_name,@key_str, @init_vector),"
                              "AES_DECRYPT(last_name,@key_str, @init_vector),"
                              "AES_DECRYPT(Address,@key_str, @init_vector),"
                              "AES_DECRYPT(Phone_Number,@key_str, @init_vector),"
                              "from %s;")
            await cur.execute(befor_select_all)
            await conn.commit()

            await cur.execute(select_special, create_table4customer)

            await conn.commit()

            result_db = await cur.fetchall()
            
            for characteristics in result_db:
                dic_user_id[kwargs["ch_customer_acc"]] = characteristics[1]
                dic_user_name[kwargs["ch_customer_acc"]] = characteristics[2]
                dic_first_name[kwargs["ch_customer_acc"]] = characteristics[3]
                dic_last_name[kwargs["ch_customer_acc"]] = characteristics[4]
                dic_Address[kwargs["ch_customer_acc"]] = characteristics[5]
                dic_Phone_Number[kwargs["ch_customer_acc"]] = characteristics[6]

        elif flag_DB_Table == "mem2db_customer":            
            save_in_customer_table = ("""SET block_encryption_mode = 'aes-256-cbc'; 
                                      SET @key_str = SHA2('My secret passphrase',512);
                                      SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; 
                                      INSERT IGNORE INTO {table4customer}(user_id, first_name, last_name, Address, Phone_Number)
                                      VALUES(AES_ENCRYPT('{user_id}',@key_str, @init_vector),
                                      AES_ENCRYPT('{first_name}',@key_str, @init_vector),
                                      AES_ENCRYPT('{last_name}',@key_str, @init_vector),
                                      AES_ENCRYPT('{Address}',@key_str, @init_vector),
                                      AES_ENCRYPT('{Phone_Number}',@key_str, @init_vector)) 
                                      ON DUPLICATE KEY UPDATE 
                                      user_id = '{user_id}';""")

            table_customer = {"table4customer" : table4customer, "user_id" : dic_user_id.get(kwargs["key_acc"]),
                              "first_name" : dic_first_name.get(kwargs["key_acc"]),
                              "last_name" : dic_last_name.get(kwargs["key_acc"]),
                              "Address" : dic_Address.get(kwargs["key_acc"]),
                              "Phone_Number" : dic_Phone_Number.get(kwargs["key_acc"])}

            await cur.execute(create_customer_table)
            await conn.commit()
            await cur.execute(save_in_customer_table.format(**table_customer))
            await conn.commit()


        elif flag_DB_Table == "give_price_from_title4customer":
            give_p_c4customer = ("""select AES_DECRYPT(currency_ware,@key_str, @init_vector),
                              AES_DECRYPT(discount,@key_str, @init_vector)
                              from sec_sell_{table_number} where AES_DECRYPT(title,@key_str, @init_vector) = '{title}';""")
            await cur.execute(befor_select_all)
            await conn.commit()

            await cur.execute(give_p_c4customer.format(table_number = kwargs["table_name"], title = kwargs["title_of_product"]))
            await conn.commit()

            result_db = await cur.fetchall()
            
            if not result_db[0][0]:
                return None , result_db[0][1].decode('utf8')
            elif not result_db[0][1]:
                return result_db[0][0].decode('utf8'), None
            else:
                return result_db[0][0].decode('utf8'), result_db[0][1].decode('utf8')
        await cur.close()
    conn.close()
