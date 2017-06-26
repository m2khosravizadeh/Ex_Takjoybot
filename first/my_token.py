import sys
import asyncio

from .Simple import first_token
from .MessageTexts import *
from .db_takjoy import db4takjoy
from ..secound.Principle import main
from ..secound.db4close_store import close_store_Funnc

TOKEN = sys.argv[1]  
give_token = 1

Bot_Token[0] = TOKEN

async def first_def():
    await db4takjoy(1)
    await close_store_Funnc(2)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(first_def())
    loop.create_task(main(TOKEN))
    loop.run_forever()
