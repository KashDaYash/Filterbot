from config import OWNER
from pyrogram import filters
from yash import app
from config import *

HELP_TEXT = f'''😇How To use  me

press /buy to purchase a subscription.

Index a group with - /index 
EXAMPLE: /index -100xxxxxxxxxxx
Add me in the channel. And make sure I have all the permissions!


Remove a Channel with - /remove -100xxxxxxxxxxx
this will help you to remove a indexed channel from your group.


Get indexed channels list with - /viewlist 

Check your information with - /info
Gives your information and validity of your subscription

Get ID of current chat - /id

Auto_delete : use /autodel command to enable or disable
              auto message delete system.
'''




@app.on_message(filters.command("help"))
async def help_handler(app, message):
    chat_id = message.chat.id
    await message.reply(HELP_TEXT)
  
@app.on_message(filters.command("id"))
async def id_handle(app , message):
    chat_id = message.chat.id
    user = message.from_user
    MSG = f"This Chat ID : `{chat_id}`\n"
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        MSG += f"Reply User ID: `{user_id}`"
    elif message.from_user:
        user_id = message.from_user.id
        MSG += f"Your ID: `{user_id}`"
    else:
        None
    await message.reply(MSG)

TEXT = f'''This bot is made by @{OWNER} A full time python developer

Our channel :- @movie_artss
Our selling channel :- @platimostore

Want to make any kind of bot & tool dm @{OWNER}'''

@app.on_message(filters.command("about"))
async def about_handle(_,message):
    chat_id = message.chat.id
    await message.reply(TEXT)