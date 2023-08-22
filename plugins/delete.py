import asyncio
from db import *
from config import *
from time import time
from bot import dbot as bot
import time 
from datetime import datetime 

PLAN = ""
'''async def check_up(bot):   
    _time = int(time.time()) 
    all_data = await get_all_dlt_data(_time)
    for data in all_data:
        try:
           await bot.delete_messages(chat_id=data["chat_id"],
                                     message_ids=data["message_id"])           
        except Exception as e:
           err=data
           err["❌ Error"]=str(e)
           print(err)
    await delete_all_dlt_data(_time)

async def run_check_up():
    async with bot: 
        while True:  
           await check_up(bot)
           await asyncio.sleep(1)'''

async def plan_update():
  while True:
    _time = int(time.time())
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = current_date.strftime("%Y-%m-%d")
    info_data = await see_plan(_time)
    print(info_data)
    for data in info_data: 
      try:
        id = data["_id"]
        user_id = data["user_id"]
    
        await update_group(id, new_data={"verified": False, "plan": PLAN})
        msg = await bot.send_message(id, f"Your Plan Expired Today Now Contact To My Owner @{OWNER}")
        await bot.pin_chat_message(
    id,
    message_id=msg.id
)
      except Exception as e:
        await bot.send_message(OWNER,e)
    

bot.start()
#asyncio.create_task(run_check_up())
asyncio.create_task(plan_update())
