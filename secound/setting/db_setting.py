import datetime
import asyncio
import aiomysql

from .setting_constants import *
from ..secound_constants import *

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
    result_db = None
    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
                              user='root', password="lk1l,tr3ldal5",charset = "utf8",
                              db='Test', loop=loop)

    cur = await conn.cursor()

    table4customer = "sec_customer_" + str(kwargs["table_name"])
    table4order = "flag4order_" + str(kwargs["table_name"])
    table_seller_name = 'sec_sell_' + str(kwargs["table_name"])
    create_customer_table = ("CREATE TABLE IF NOT EXISTS " + table4customer + " ("
                             "`emp_nu` int(12) NOT NULL AUTO_INCREMENT,"
                             "`user_id` Text NULL,"
                             "`user_name` Text NULL,"
                             "`first_name` Text NULL,"
                             "`last_name` Text NULL,"
                             "`Address` Text NULL,"
                             "`Phone_Number` Text NULL,"
                             "`Sphere1` Text NULL,"
                             "`Sphere2` Text NULL,"
                             "PRIMARY KEY(emp_nu));")

    create_order_table = ("CREATE TABLE IF NOT EXISTS " + table4order + " ("
                          "`emp_nu` int(12) NOT NULL AUTO_INCREMENT,"
                          "`title` Text NULL,"
                          "PRIMARY KEY(emp_nu));")



    create_table_seller = ("CREATE TABLE IF NOT EXISTS " + table_seller_name + " ("
                           "`emp_nu` int(12) NOT NULL AUTO_INCREMENT,"
                           "`first_button` Text NULL,"
                           "`secound_button` Text NULL,"
                           "`title` Text NULL,"
                           "`context` Text NULL,"
                           "`price_ware` Text NULL,"
                           "`currency_ware` Text NULL,"
                           "`unit_ware` Text NULL,"
                           "`discount` Text NULL,"
                           "`photo_file` Text NULL,"
                           "`file_id` Text NULL,"
                           "`showindays` Text NULL,"
                           "PRIMARY KEY(emp_nu));")

    async with conn.cursor() as cur:    
        await cur.execute(create_customer_table)
        await conn.commit()
        await cur.execute(create_order_table)
        await conn.commit()
        await cur.execute(create_table_seller)
        await conn.commit()


        if flag_DB_Table == "delete_box":

            delinbox = ("""SET block_encryption_mode = 'aes-256-cbc';
                        SET @key_str = SHA2('My secret passphrase',512);
                        SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; 
                        delete from {table_seller_name} where title = AES_ENCRYPT('{Title}', @key_str, @init_vector);""".format(table_seller_name = table_seller_name, Title = kwargs["title"]))
            await cur.execute(delinbox)
            await conn.commit()


        elif flag_DB_Table == "Product_finished":

            save_in_order_table = ("""SET block_encryption_mode = 'aes-256-cbc'; 
                                   SET @key_str = SHA2('My secret passphrase',512);
                                   SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; 
                                   INSERT IGNORE INTO {table4order}(`title`)
                                   VALUES(AES_ENCRYPT('{Table_in}',@key_str, @init_vector));""".format(table4order = table4order, Table_in = kwargs["title"]))

            await cur.execute(save_in_order_table)
            await conn.commit()


        elif flag_DB_Table == "Product_Exists":

            remove_from_order_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';  
                                       delete from {table4order} where `title` = AES_ENCRYPT('{title_in}', @key_str, @init_vector);""".format(table4order = table4order, title_in = kwargs["title"]))

            await cur.execute(remove_from_order_table)
            await conn.commit()


        elif flag_DB_Table == "Product_Check":

            check_order_table = ("""select AES_DECRYPT(`title`,@key_str, @init_vector) from {my_table};""".format(my_table=table4order))
            
            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(check_order_table)
            await conn.commit()
            result_db = None
            result_db = await cur.fetchall()
            return result_db


        elif flag_DB_Table == "Title_check_Box_choose":

            save_in_order_table = ("""select AES_DECRYPT(`title`,@key_str, @init_vector),
                                   AES_DECRYPT(`context`,@key_str, @init_vector),
                                   AES_DECRYPT(`price_ware`,@key_str, @init_vector),
                                   AES_DECRYPT(`currency_ware`,@key_str, @init_vector),
                                   AES_DECRYPT(`unit_ware`,@key_str, @init_vector),
                                   AES_DECRYPT(`discount`,@key_str, @init_vector),
                                   AES_DECRYPT(`photo_file`,@key_str, @init_vector),
                                   AES_DECRYPT(`file_id`,@key_str, @init_vector),
                                   AES_DECRYPT(`showindays`,@key_str, @init_vector) from {sec_sell} where `title` = AES_ENCRYPT('{Title_in}',@key_str, @init_vector);""".format(sec_sell = table_seller_name, Title_in = kwargs["title"]))
            

            await cur.execute(befor_select_all)
            await conn.commit()
            result_db = None
            
            await cur.execute(save_in_order_table)
            await conn.commit()
            result_db = await cur.fetchall()

            flag_Box = 0
            BOX_Dict = {}
            BOX_Dict_Temp = {}
            for row in result_db:
                BOX_Temp = {}
            
                for i in range(0, 8):
                    if row[i]:

                        BOX_Dict[BoxList[i]] = row[i].decode("utf-8")




            return BOX_Dict


        elif flag_DB_Table == "Addnewkey":

            addnewkey = ("SET block_encryption_mode = 'aes-256-cbc';"
                         "SET @key_str = SHA2('My secret passphrase',512); "
                         "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; "
                         "SET @ENCRYPT_first_button = %s; "
                         "INSERT IGNORE INTO " + table_seller_name + "(first_button) VALUES(AES_ENCRYPT(@ENCRYPT_first_button,@key_str, @init_vector));")

            table4seller = (str(kwargs["firstkey"]))

            await cur.execute(addnewkey, (str(kwargs["firstkey"])))
            await conn.commit()


        elif flag_DB_Table == "delete1key":
            remove_from_order_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';  
                                       delete from """ + table_seller_name + " where `first_button` = AES_ENCRYPT(%s, @key_str, @init_vector);")

            await cur.execute(remove_from_order_table, kwargs["first_button"])
            await conn.commit()


        elif flag_DB_Table == "delete2key":
            remove_from_order_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';  
                                       delete from """ + table_seller_name + " where `secound_button` = AES_ENCRYPT(%s, @key_str, @init_vector);")

            await cur.execute(remove_from_order_table, kwargs["secound_button"])
            await conn.commit()


        elif flag_DB_Table == "edit1key":
            remove_from_order_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';  
                                       UPDATE """ + table_seller_name + " set `first_button` = AES_ENCRYPT(%s, @key_str, @init_vector) where `first_button` = AES_ENCRYPT(%s, @key_str, @init_vector);")

            await cur.execute(remove_from_order_table, (kwargs["new_key"], kwargs["ex_key"]))
            await conn.commit()
            return


        elif flag_DB_Table == "edit2key":
            remove_from_order_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';
                                       UPDATE """ + table_seller_name + " set `secound_button` = AES_ENCRYPT(%s, @key_str, @init_vector) where `secound_button` = AES_ENCRYPT(%s, @key_str, @init_vector);")

            await cur.execute(remove_from_order_table, (kwargs["new_key"], kwargs["ex_key"]))
            await conn.commit()
            return

        
        elif flag_DB_Table == "Addnewkey2":
            addnewkey2 = ("SET block_encryption_mode = 'aes-256-cbc';"
                          "SET @key_str = SHA2('My secret passphrase',512); "
                          "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; "
                          "SET @keyOfBox = %s; "
                          "SET @key2OfBox = %s; "
                          "INSERT IGNORE INTO "+ table_seller_name + "(first_button, secound_button)"
                          "VALUES(AES_ENCRYPT(@keyOfBox, @key_str, @init_vector),AES_ENCRYPT(@key2OfBox, @key_str, @init_vector))")
                                                                                                                                           
            await cur.execute(addnewkey2, (kwargs["firstkey"],kwargs["secoundkey"]))
            await conn.commit()

            
        elif flag_DB_Table == "db2mem_BOX":
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
            

            await cur.execute(befor_select_all)
            await conn.commit()
            result_db = None
            
            await cur.execute(select_all)

            await conn.commit()

            result_db = await cur.fetchall()

            flag_Box = 0
            key_Box_Dict = {}
            BOX_Dict = {}
            BOX_Dict['key'] = {}
            BOX_Dict['main'] = []
            BOX_Dict_Temp = {}
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


            return BOX_Dict, key_Box_Dict

        
        elif flag_DB_Table == "changeproductindb":
            changeindb = ("update sec_sell_{table_name} set {goal} = AES_ENCRYPT('{pr}',@key_str, @init_vector) where `title` = AES_ENCRYPT('{title_in}',@key_str, @init_vector)")

            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(changeindb.format(table_name = kwargs["table_name"], goal = kwargs["goal"], pr = kwargs["pr"], title_in = kwargs['extitle']))
            await conn.commit()

        elif flag_DB_Table == "take_ChosenFromTitle":
            BoxFromTitle = ("""select AES_DECRYPT(`context`,@key_str, @init_vector),
                            AES_DECRYPT(`price_ware`,@key_str, @init_vector),
                            AES_DECRYPT(`currency_ware`,@key_str, @init_vector),
                            AES_DECRYPT(`discount`,@key_str, @init_vector),
                            AES_DECRYPT(`file_id`,@key_str, @init_vector)
                            from sec_sell_{t_num} where title = AES_ENCRYPT('{t_in}',@key_str, @init_vector)
                            """)

            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(BoxFromTitle.format(t_num = kwargs["table_name"], t_in = kwargs['t_in']))
            await conn.commit()

            result4TBFT = kwargs['t_in'] + "\n\n"
            result_db = await cur.fetchall()
            if result_db:
                return result_db[0][0], result_db[0][1], result_db[0][2], result_db[0][3], result_db[0][4]

        elif flag_DB_Table == "take_BoxFromTitle":
            BoxFromTitle = ("""select AES_DECRYPT(`context`,@key_str, @init_vector),
                            AES_DECRYPT(`price_ware`,@key_str, @init_vector),
                            AES_DECRYPT(`currency_ware`,@key_str, @init_vector),
                            AES_DECRYPT(`discount`,@key_str, @init_vector)
                            from sec_sell_{t_num} where title = AES_ENCRYPT('{t_in}',@key_str, @init_vector)
                            """)

            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(BoxFromTitle.format(t_num = kwargs["table_name"], t_in = kwargs['t_in']))
            await conn.commit()

            result4TBFT = kwargs['t_in'] + "\n\n"
            result_db = await cur.fetchall()
            if result_db:
                for row in result_db:
                    if row[0]:
                        result4TBFT += row[0].decode("utf-8") + "\n\n"
                    if row[1]:
                        result4TBFT +=  "قیمت: " + row[1].decode("utf-8") + " " + row[2].decode("utf-8") + "\n"
                    if row[3]:
                         row3 = row[3].decode("utf-8")
                         result4TBFT += "تخفیف: " + row3 + "درصد \n\n"
                         final_price = str(int((100 - int(row3)) * int(row[1].decode("utf-8"))/100))
                         result4TBFT += "قیمت نهایی: " + final_price + " " + row[2].decode("utf-8") + "\n"
            
            return result4TBFT

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
            
            save_in_customer_table = ("SET block_encryption_mode = 'aes-256-cbc'; "
                                      "SET @key_str = SHA2('My secret passphrase',512);"
                                      "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; "
                                      "INSERT IGNORE INTO "+ table4customer +"("
                                      "user_id, username, first_name, last_name, Address, Phone_Number)"
                                      "VALUES(AES_ENCRYPT(%s,@key_str, @init_vector),"
                                      "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                      "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                      "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                      "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                      "AES_ENCRYPT(%s,@key_str, @init_vector));")
            
            table_customer = (dic_user_id.get(kwargs["key_acc"]),
                              dic_username.get(kwargs["key_acc"]),
                              dic_first_name.get(kwargs["key_acc"]),
                              dic_last_name.get(kwargs["key_acc"]),
                              dic_Address.get(kwargs["key_acc"]),
                              dic_Phone_Number.get(kwargs["key_acc"]))

            await cur.execute(create_customer_table)
            await conn.commit()
            await cur.execute(save_in_customer_table, table_customer)
            await conn.commit()

        await cur.close()
    conn.close()
        
