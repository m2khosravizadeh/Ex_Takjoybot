import asyncio
import aiomysql

from .MessageTexts import *
from ..secound.secound_constants import *
from ..secound.Seller.const4seller import *
from ..secound.Seller.constdb4dbseller import *

async def db4takjoy(flag_Update_Token, **kwargs):
    pre_secure = """SET block_encryption_mode = 'aes-256-cbc'; 
                 SET @key_str = SHA2('My secret passphrase',512);
                 SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; """  
    db2mem_citypost = ("""select AES_DECRYPT(`city_name`,@key_str, @init_vector), AES_DECRYPT(`post_purchase`,@key_str, @init_vector) from {table4citypost};""")
    createtable4citypost = ("""CREATE TABLE IF NOT EXISTS {table4citypost}(
                         `citypost_no` int(12) NOT NULL AUTO_INCREMENT,
                         `city_name` Text not NULL,
                         `post_purchase` Text not NULL,
                         PRIMARY KEY(citypost_no));""")
    select4customer = ("""select AES_DECRYPT(user_id,@key_str, @init_vector),
                      AES_DECRYPT(user_name,@key_str, @init_vector),
                      AES_DECRYPT(first_name,@key_str, @init_vector),
                      AES_DECRYPT(last_name,@key_str, @init_vector),
                      AES_DECRYPT(Address,@key_str, @init_vector),
                      AES_DECRYPT(Phone_Number,@key_str, @init_vector)
                      from {table4customer};""")
    create_customer_table = ("""CREATE TABLE IF NOT EXISTS {table4customer}(
                             `emp_nu` int(12) NOT NULL AUTO_INCREMENT,
                             `user_id` Text NULL,
                             `user_name` Text NULL,
                             `first_name` Text NULL,
                             `last_name` Text NULL,
                             `Address` Text NULL,
                             `Phone_Number` Text NULL,
                             `city_dict` Text NULL,
                             `Postal_code` Text NULL,
                             PRIMARY KEY(emp_nu));""")
    update_token = ("""SET block_encryption_mode = 'aes-256-cbc';
                       SET @key_str = SHA2('My secret passphrase',512); 
                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';
                       SET @ENCRYPT_Bot_id = '{Bot_id}';
                       SET @ENCRYPT_Token = '{Token}';
                       UPDATE Token_Takjoy set `Token` = AES_ENCRYPT(@ENCRYPT_Token, @key_str, @init_vector) where `Bot_id` = AES_ENCRYPT(@ENCRYPT_Bot_id, @key_str, @init_vector);""")

    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
                                  user='root', password="lk1l,tr3ldal5",charset = "utf8",
                                  db='Test', loop=loop)

    cur = await conn.cursor()
    async with conn.cursor() as cur:    
        await cur.execute(sql)
        await conn.commit()
        if flag_Update_Token == 0:
            cur = await conn.cursor()
            insert_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                            SET @key_str = SHA2('My secret passphrase',512); 
                            SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; 
                            SET @ENCRYPT_User_id = '{User_id}'; 
                            SET @ENCRYPT_Bot_id = '{Bot_id}'; 
                            SET @ENCRYPT_Token = '{Token}'; 
                            INSERT IGNORE INTO Token_Takjoy(User_id, Token, Bot_Date, Bot_ID) 
                            VALUES(AES_ENCRYPT(@ENCRYPT_User_id,@key_str, @init_vector), 
                            AES_ENCRYPT(@ENCRYPT_Token,@key_str, @init_vector), 
                            (CURDATE() + interval {Daysetting} day), 
                            AES_ENCRYPT(@ENCRYPT_Bot_id,@key_str, @init_vector));""")
    
            len_flag = len(saveindb)
            for i in range(0,len_flag):
                my_user_id = saveindb.pop()
                await cur.execute(insert_table.format(User_id = str(my_user_id),
                                                      Token = true_token[my_user_id], 
                                                      Bot_id = kwargs["Bot_id"], 
                                                      Daysetting = int(kwargs["Daysetting"])))
                await conn.commit()    

        elif flag_Update_Token == 1:            
            await cur.execute(befor_select_all)
            await conn.commit()
            await cur.execute(select_all)
            await conn.commit()
            result_db = await cur.fetchall()
            await cur.execute(select4botmaker)
            await conn.commit()
            curbing_repeat_bot = await cur.fetchall()
            for row in curbing_repeat_bot:
                if row[0] and row[1]:
                    dic_bot_user_id[row[0].decode('utf8')] = row[1].decode('utf8')
                    dic_user_id_bot[row[1].decode('utf8')] = row[0].decode('utf8')
                    if row[1].decode('utf8') not in list_bot_id:
                        list_bot_id.append(row[1].decode('utf8'))
            await cur.execute(select4chargebot)
            await conn.commit()
            db2mem4charge_bot =  await cur.fetchall()
            for row in db2mem4charge_bot:
                if row[1] and row[0]:
                    dic4charge_bot_id2token[row[1].decode('utf8')] = row[0].decode('utf8')

            for row in result_db:
                if row[1]:
                    row1 = row[1].decode('utf8')
                    row2 = row[2].decode('utf8')
                    temp_bot_un = row[4].decode('utf8')
                    temp_bot_date = row[3]
                    if row1:
                        if row1 not in dict4bot_ids4users:
                            dict4bot_ids4users[row1] = []
                    if temp_bot_un not in dict4bot_ids4users[row1]:
                        dict4bot_ids4users[row1].append(temp_bot_un)

                    Date_bot[temp_bot_un] = temp_bot_date
                    user_id4owner[row2] = str(row1) + row2
                    UNT_Dict[row[0]] = [row1, row2, temp_bot_date]
                    await cur.execute(createtable4seller.format(table4seller = row[0]))
                    await cur.execute(select_all_seller.format(table4seller = row[0]))
                    await conn.commit()
                    result_sellers = await cur.fetchall()
                    seller_dict[row1 + row2] = []
                    for seller_row in result_sellers:
                        seller_row1 = seller_row0 = None
                        if seller_row[1]:
                            seller_row1 = seller_row[1].decode('utf8')
                        if seller_row[0]:
                            seller_row0 = seller_row[0].decode('utf8')
                        seller_dict[row1 + row2].append([seller_row1, seller_row0])
                    table4citypost = "post4city_" + str(row[0])
                    await cur.execute(createtable4citypost.format(table4citypost = table4citypost))
                    await conn.commit()
                    await cur.execute(db2mem_citypost.format(table4citypost = table4citypost))
                    await conn.commit()
                    citypost_iter = await cur.fetchall()
                    for citypost in citypost_iter:
                        if citypost[0] and citypost[1]:
                            citypost_0 = citypost[0].decode('utf8') 
                            citypost_1 = citypost[1].decode('utf8')
                            if row[0] not in dict_citypost:
                                dict_citypost[row[0]] = []
                            dict_citypost[row[0]].append([citypost_0, citypost_1])
                    table4customer = "sec_customer_" + str(row[0])
                    await cur.execute(create_customer_table.format(table4customer = table4customer))
                    await conn.commit()
                    await cur.execute(select4customer.format(table4customer = table4customer))
                    await conn.commit()
                    iter4customer_chars = await cur.fetchall()
                    for customer_chars in iter4customer_chars:
                        if row[0] not in dic_user_id:
                            dic_user_id[row[0]] = []
                        dic_user_id[row[0]].append(customer_chars[0].decode('utf8'))
                        for index in range(1, len(customer_chars)-1):
                            if customer_chars[index]:
                                list4customer_chars[index-1][customer_chars[0].decode('utf8') + row2] = customer_chars[index].decode('utf8')
                    dict_token2e_num[row2] = row[0]
            else:
                return True

        elif flag_Update_Token == 2:
            for U_id in changeindb:
                Temp_Exchange_Token = save_new_token[U_id]
                Exchange_Token = (U_id, Temp_Exchange_Token[1])
                await cur.execute(Update_Token, Exchange_Token)
                await conn.commit()

        elif flag_Update_Token == 3:
            create_table_seller = "sec_sell_" + str(kwargs["table_name"])
            temp_key = kwargs["key_acc"]
            table_seller = (dic_first_button.get(temp_key),
                            dic_secound_button.get(temp_key),
                            dic_title.get(temp_key),
                            dic_context.get(temp_key),
                            dic_price_ware.get(temp_key),
                            dic_currency_ware.get(temp_key),
                            dic_unit_ware.get(temp_key),
                            dic_discount.get(temp_key),
                            dic_photo_file.get(temp_key),
                            file_id.get(temp_key),
                            day_code.get(temp_key))

            create_other_table = ("CREATE TABLE IF NOT EXISTS " + create_table_seller + " ("
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

            save_in_other_table = ("SET block_encryption_mode = 'aes-256-cbc'; "
                                "SET @key_str = SHA2('My secret passphrase',512);"
                                "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; "
                                "INSERT IGNORE INTO "+create_table_seller+"("
                                "first_button, secound_button, title, context, currency_ware, price_ware, unit_ware, discount, photo_file, file_id, showindays)"
                                "VALUES(AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector),"
                                "AES_ENCRYPT(%s,@key_str, @init_vector));")

            await cur.execute(create_other_table)
            await conn.commit()
            await cur.execute(save_in_other_table, table_seller)
            await conn.commit()

        elif flag_Update_Token == "chang_token":
            await cur.execute(update_token.format(Bot_id = kwargs["bot_id"], Token = kwargs["new_token"]))
            await conn.commit()

        elif flag_Update_Token == "give_bot_id4ch_t":
            give_bot_id = """SET @ENCRYPT_User_id = '{User_id}'; 
                          select AES_DECRYPT(Bot_ID,@key_str, @init_vector) from Token_Takjoy where @ENCRYPT_User_id = AES_DECRYPT(User_id, @key_str, @init_vector);"""
            await cur.execute(pre_secure)
            await conn.commit()
            await cur.execute(give_bot_id.format(User_id = str(kwargs["user_id"])))
            await conn.commit()
            result_bot_names = await cur.fetchall()
            return result_bot_names

        elif flag_Update_Token == "charge_bot":
            charge_bot_table = """SET @ENCRYPT_Bot_id = '{Bot_id}';
                                  UPDATE Token_Takjoy SET `Bot_Date` = DATE_ADD(`Bot_Date` , INTERVAL {Daysetting} DAY)
                                  where Bot_id = AES_ENCRYPT(@ENCRYPT_Bot_id,@key_str, @init_vector)"""
            await cur.execute(pre_secure)
            await conn.commit()
            await cur.execute(charge_bot_table.format(Bot_id = kwargs["bot_id"], Daysetting = str(kwargs["day"])))
            await conn.commit()
            return

        elif flag_Update_Token == "create_db4citypost":
            table4citypost = "post4city_" + str(kwargs["table_name"])
            createtable4citypost = ("""CREATE TABLE IF NOT EXISTS {table4citypost}(
                                     `citypost_no` int(12) NOT NULL AUTO_INCREMENT,
                                     `city_name` Text not NULL,
                                     `post_purchase` Text not NULL,
                                     PRIMARY KEY(citypost_no));""")
            save_in_citypost = ("""INSERT IGNORE INTO {table4citypost}(city_name, post_purchase)
                                VALUES(AES_ENCRYPT('{city_name}',@key_str, @init_vector),
                                AES_ENCRYPT('{post_purchase}',@key_str, @init_vector));""")
            await cur.execute(pre_secure)
            await conn.commit()
            await cur.execute(createtable4citypost.format(table4citypost = table4citypost))
            await conn.commit()
            await cur.execute(save_in_citypost.format(table4citypost = table4citypost, city_name = kwargs["city_name"], post_purchase = kwargs["post_purchase"]))
            await conn.commit()

        elif flag_Update_Token == "db4citypost":
            table4citypost = "post4city_" + str(kwargs["table_name"])
            createtable4citypost = ("""CREATE TABLE IF NOT EXISTS {table4citypost}(
                                     `citypost_no` int(12) NOT NULL AUTO_INCREMENT,
                                     `city_name` Text not NULL,
                                     `post_purchase` Text not NULL,
                                     PRIMARY KEY(citypost_no));""")
            take_from_citypost = ("""select AES_DECRYPT(city_name,@key_str, @init_vector),
                                AES_DECRYPT(post_purchase,@key_str, @init_vector)
                                from {table4citypost};""")
            edit_citypost = ("""update {table4citypost} set `city_name` = AES_ENCRYPT('{city_name}',@key_str, @init_vector),
                               `post_purchase` = AES_ENCRYPT('{city_name}',@key_str, @init_vector) where
                               `city_name` = AES_ENCRYPT('{ex_city_name}',@key_str, @init_vector);""")
            delete_citypost = ("""DELETE FROM {table4citypost} where `city_name` = AES_ENCRYPT('{city_name}',@key_str, @init_vector);""")
            await cur.execute(pre_secure)
            await conn.commit()
            await cur.execute(createtable4citypost.format(table4citypost = table4citypost))
            await conn.commit()            
            if kwargs['ctrl_account'] == "take_from_citypost":
                await cur.execute(take_from_citypost.format(table4citypost = table4citypost))
                await conn.commit()
                result_sellers = await cur.fetchall()
                return result_sellers                
            elif kwargs['ctrl_account'] == "edit_citypost":
                await cur.execute(edit_citypost.format(table4citypost = table4citypost, city_name = kwargs["city_name"], post_purchase = kwargs["purchaseofcity"], ex_city_name = kwargs["ex_city_name"]))
                await conn.commit()
            elif kwargs['ctrl_account'] == "delete_citypost":
                await cur.execute(delete_citypost.format(table4citypost = table4citypost, city_name = kwargs["city_name"]))
                await conn.commit()            

        elif flag_Update_Token =="account_db":
            table4account = "account_" + str(kwargs["table_num"])
            createtable4citypost = ("""CREATE TABLE IF NOT EXISTS {table4account}(
                                 `account_no` int(12) NOT NULL AUTO_INCREMENT,
                                 `account_num` Text not NULL,
                                 `account_name` Text not NULL,
                                 PRIMARY KEY(account_no));""")
            save_in_citypost = ("""INSERT IGNORE INTO {table4account}(account_num, account_name)
                                VALUES(AES_ENCRYPT('{account_num}',@key_str, @init_vector),
                                AES_ENCRYPT('{account_name}',@key_str, @init_vector));""")
            take_from_db = ("""select AES_DECRYPT(`account_num`,@key_str, @init_vector) from {table4account};""")
            take_all_from_db = ("""select AES_DECRYPT(`account_num`,@key_str, @init_vector), AES_DECRYPT(`account_name`,@key_str, @init_vector) from {table4account};""")
            Delete_from_db = ("""Delete from {table4account} where '{account_num}' = AES_DECRYPT(`account_num`,@key_str, @init_vector);""")
            await cur.execute(pre_secure)
            await conn.commit()
            await cur.execute(createtable4citypost.format(table4account = table4account))
            await conn.commit()
            result_db = await cur.fetchall()
            if kwargs['ctrl_account'] == "save_in_db":
                await cur.execute(save_in_citypost.format(table4account = table4account, account_num = kwargs["account_num"], account_name = kwargs["account_name"]))
                await conn.commit()
            elif kwargs['ctrl_account'] == "take_from_db":
                await cur.execute(take_from_db.format(table4account = table4account))
                await conn.commit()
                result_account = await cur.fetchall()
                Temp_account = []
                for accounts in result_account:
                    Temp_account.append(accounts[0].decode('utf8'))
                return Temp_account
            elif kwargs['ctrl_account'] == "Delete_from_db":
                await cur.execute(Delete_from_db.format(table4account = table4account, account_num = kwargs["account_num"]))
                await conn.commit()
            elif kwargs['ctrl_account'] == "take_all_from_db":
                await cur.execute(take_all_from_db.format(table4account = table4account))
                await conn.commit()
                result_all_account = await cur.fetchall()
                return result_all_account
    await cur.close()
    conn.close()
