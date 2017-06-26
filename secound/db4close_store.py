import asyncio
import aiomysql

from ..first.MessageTexts import *
from .secound_constants import *
from .constdb4close_store import *

async def close_store_Funnc(flag_Update_Token, **kwargs):

    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
                                  user='root', password="lk1l,tr3ldal5",charset = "utf8",
                                  db='Test', loop=loop)

    cur = await conn.cursor()

    async with conn.cursor() as cur:    
        await cur.execute(sqlـstore)
        await conn.commit()
        if flag_Update_Token == 0:

            cur = await conn.cursor()
            insert_table = ("SET block_encryption_mode = 'aes-256-cbc';"
                            "SET @key_str = SHA2('My secret passphrase',512);"
                            "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';"
                            "SET @ENCRYPT_stores = %s;"
                            "INSERT IGNORE INTO close_store_table(`stores`) VALUES(AES_ENCRYPT(@ENCRYPT_stores,@key_str, @init_vector));")
            
            await cur.execute(insert_table, kwargs["Store_Specifications"])
            await conn.commit()    

        elif flag_Update_Token == 1:

            deletion_from_table = ("SET block_encryption_mode = 'aes-256-cbc';"
                            "SET @key_str = SHA2('My secret passphrase',512);"
                            "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~';"
                            "SET @ENCRYPT_stores = %s;"
                            "DELETE FROM close_store_table WHERE stores = AES_ENCRYPT(@ENCRYPT_stores,@key_str, @init_vector)")

            await cur.execute(deletion_from_table, kwargs["Store_Specifications"])
            await conn.commit()

        elif flag_Update_Token == 2:
            await cur.execute(befor_select_all_store)
            await conn.commit()


            await cur.execute(select_all_store)

            table_stores = await cur.fetchall()

            if table_stores:
                for store in table_stores[0]:
                    close_store.append((store).decode('ascii'))

            
        elif flag_Update_Token == "check_title_repetitive":
            create_table_seller = "sec_sell_" + str(kwargs["table_name"])

            await cur.execute(befor_select_all_store)
            await conn.commit()            

            await cur.execute(table_check.format(column = kwargs["column"], table_seller = create_table_seller))
            await conn.commit()


            titles = await cur.fetchall()
            return titles

            
        await cur.close()
    conn.close()
