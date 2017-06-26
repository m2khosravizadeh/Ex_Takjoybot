import asyncio
import telepot
import telepot.aio
import aiomysql

pre_secure = """SET block_encryption_mode = 'aes-256-cbc'; 
             SET @key_str = SHA2('My secret passphrase',512);
             SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; """ 

take_table = "select AES_DECRYPT(`Token`,@key_str, @init_vector) from Token_Takjoy"

give_table = """update Token_Takjoy set Bot_id = AES_ENCRYPT('{Bot_id}', @key_str, @init_vector)
                where Token = AES_ENCRYPT('{token}', @key_str, @init_vector)"""

async def first_def():
    conn = await aiomysql.connect(host = '127.0.0.1', port=3306, 
                                  user = 'root', password = "lk1l,tr3ldal5",charset = "utf8",
                                  db = 'Test', loop=loop)

    cur = await conn.cursor()
    async with conn.cursor() as cur:    
		
        await cur.execute(pre_secure)
        await conn.commit()
        await cur.execute(take_table)
        await conn.commit()

        asp = await cur.fetchall()
        for row in asp:
            print("asp is: ", asp)
            bot_intrance = telepot.Bot(row[0].decode("utf8"))
            my_bot_intrance = bot_intrance.getMe()
            await cur.execute(give_table.format(Bot_id = my_bot_intrance["username"], token = row[0].decode('utf8')))
            await conn.commit()        


loop = asyncio.get_event_loop()
loop.run_until_complete(first_def())
