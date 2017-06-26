import asyncio
import aiomysql

from ...first.MessageTexts import *
from ..secound_constants import *
from .constdb4dbseller import *

async def sellerdb(flag4sellers, **kwargs):

    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
                              user='root', password="lk1l,tr3ldal5",charset = "utf8",
                              db='Test', loop=loop)

    cur = await conn.cursor()

    async with conn.cursor() as cur:
        if flag4sellers == "sellernames":
            await cur.execute(befor_select_all_seller)
            await conn.commit()
            await cur.execute(createtable4seller.format(table4seller = kwargs["tablenumber"]))
            await conn.commit()
            await cur.execute(select_all_seller.format(table4seller = kwargs["tablenumber"]))
            await conn.commit()
            
            table_sellers = await cur.fetchall()
            sellers = []
            if table_sellers:
                for table_seller in tablesellers:
                    seller_temp = [table_seller[1]]
                    seller_temp.append(table_seller[0])
                    sellers.append(seller_temp)
                return sellers
            else:
                return None
            
            #Seller_Endorsement
        elif flag4sellers == "Seller_Endorsement":
            insert_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                            SET @key_str = SHA2('My secret passphrase',512); 
                            SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; 
                            SET @ENCRYPT_User_id = '{user_id_seller}'; 
                            INSERT IGNORE INTO sellercharacteristic{table4seller}(seller_uid) VALUES(AES_ENCRYPT(@ENCRYPT_User_id,@key_str, @init_vector));""")

            await cur.execute(insert_table.format(user_id_seller = kwargs['seller_uid'], table4seller = kwargs["tablenumber"]))
            await conn.commit()

        elif flag4sellers == "delete_seller":
            deletion_from_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                  SET @key_str = SHA2('My secret passphrase',512);
                                  SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';
                                  SET @ENCRYPT_User_id = '{user_id_seller}';
                                  DELETE FROM sellercharacteristic{table4seller} WHERE seller_uid = AES_ENCRYPT(@ENCRYPT_User_id,@key_str, @init_vector);""")

            await cur.execute(deletion_from_table.format(user_id_seller = kwargs["seller_uid"], table4seller = kwargs["tablenumber"]))
            await conn.commit()
        elif flag4sellers == "update_seller_id":
            update_seller_id_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';
                                       SET @ENCRYPT_User_id = '{user_id_seller}';
                                       SET @ENCRYPT_Value = '{value4seller}';
                                       UPDATE sellercharacteristic{table4seller} set `seller_value` = AES_ENCRYPT(@ENCRYPT_Value, @key_str, @init_vector) where `seller_uid` = AES_ENCRYPT(@ENCRYPT_User_id, @key_str, @init_vector);""")
    
            await cur.execute(update_seller_id_table.format(user_id_seller = kwargs["seller_uid"], value4seller = kwargs["seller_value"], table4seller = kwargs["tablenumber"]))
            await conn.commit()         
        elif flag4sellers == "update_seller_name":
            update_seller_name_table = ("""SET block_encryption_mode = 'aes-256-cbc';
                                       SET @key_str = SHA2('My secret passphrase',512); 
                                       SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';
                                       SET @ENCRYPT_User_name = '{user_name_seller}';
                                       SET @ENCRYPT_Value = '{value4seller}';
                                       UPDATE sellercharacteristic{table4seller} set seller_uid = AES_ENCRYPT(@ENCRYPT_User_id, @key_str, @init_vector) where `seller_value` = AES_ENCRYPT(@ENCRYPT_Value, @key_str, @init_vector);""")
    
            await cur.execute(update_seller_id_table.format(user_id_seller = kwargs["seller_uid"], value4seller = kwargs["seller_value"], table4seller = kwargs["tablenumber"]))
            await conn.commit()         
    await cur.close()
    conn.close()
