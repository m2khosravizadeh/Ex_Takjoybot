import asyncio
import aiomysql

from secound_constants import *

async def db4others(flag_Token4others):
    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, 
		                      user='root', password="lk1l,tr3ldal5",charset = "utf8",
		                      db='Test', loop=loop)


    cur = await conn.cursor()
    async with conn.cursor() as cur:
        if flag_Token4others == 1:
            
            await cur.execute(select_all)
            await conn.commit()
            result_db = cur.fetchall()
            for row in result_db:
                UNT_Dict[row[0]] = [row[1], row[2]]
            else:
                return True
                     

        await cur.close()
    conn.close()

            

    
    
