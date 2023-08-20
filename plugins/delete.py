from datetime import datetime, timedelta
import asyncio
from pyrogram import Client, idle
from db import *
from bot import dbot as bot


async def delete_messages():
    while True:
        try:
            # Get current time
            oki = datetime.now()
            current_time = oki.replace(second=0, microsecond=0).strftime("%y-%m-%d %H:%M")
            print(current_time)
            
            # Query MongoDB for data
            d_find = await del_find(current_time)
            if d_find and current_time >= d_find['time']:
                print(d_find)
                chat_id = d_find["chat_id"]
                message_id = d_find["message_id"]

                # Delete the message
                await bot.delete_messages(chat_id, message_id)

                # Remove the message data from MongoDB
                del_col.delete_one({"_id": d_find["_id"]})
        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(10)  # Wait for 1 minute
async def update_documents():
    while True:
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = current_date.strftime("%Y-%m-%d")
        
        # Find documents with the "plan" field less than or equal to the current date
        documents_to_update = grp_col.find({"plan": {"$lte": timestamp}})
        
        async for doc in documents_to_update:
          print(doc)
          await grp_col.update_one({"_id": doc["_id"]}, {"$set": {"verified": False}})
          user_id = doc["user_id"]  # Get the user_id from the document
          id = await grp_col.find_one({"user_id": user_id})
            
          if id:
              await bot.send_message(id["_id"], "Hey Your Plan Expired Today Now")
          else:
            await bot.send_message(OWNER_ID, f"{doc['_id']} plan expired and bot don't send message in there chat")

        await asyncio.sleep(5)  # Wait for 1 minute


bot.start()
loop = asyncio.get_event_loop()
loop.create_task(update_documents())
loop.create_task(delete_messages())
bot.idle()
