from yash import app, yk
from yash.core.db import *
from config import *
from pyrogram import *
from pyrogram.types import *

@app.on_message(filters.group & filters.command("index"))
async def connect(app, message):
    if len(message.command) == 1:
        return await message.reply("❌ Incorrect format!\nUse `/index ChannelID`", parse_mode=enums.ParseMode.MARKDOWN)
    m=await message.reply("Please wait..")
    user = yk.me
    try:
        group     = await get_group(message.chat.id)
        user_id   = group["user_id"] 
        user_name = group["user_name"]
        verified  = group["verified"]
        channels  = group["channels"].copy()
    except:
        return await app.leave_chat(message.chat.id)  
    if message.from_user.id != user_id:
        return await m.edit(f"Only @{user_name} can use this command 😁")
    if bool(verified)==False:
        return await m.edit(f"Hey {message.from_user.mention} You Didn't Purchase Any Plan !\n Contact To My Owner @{OWNER}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Buy",url=f"t.me/{OWNER}")]]))    
    try:
        channel = int(message.command[-1])
        if channel in channels:
            return await message.reply("This channel is already index! You Cant Connect Again")
        channels.append(channel)
    except:
        return await m.edit("❌ Incorrect format!\nUse `/index ChannelID`")    
    try:
        chat   = await app.get_chat(channel)
        group  = await app.get_chat(message.chat.id)
        c_link = chat.invite_link
        g_link = group.invite_link
        await yk.join_chat(c_link)
    except Exception as e:
        if "The user is already a participant" in str(e):
            pass
        else:
            text = f"❌ Error: `{str(e)}`\nMake sure I'm admin in that channel & this group with all permissions and @{(user.username or user.mention)} is not banned there"
            return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Successfully indexed to [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#NewConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await app.send_message(chat_id=LOG_CHANNEL, text=text)


@app.on_message(filters.group & filters.command("remove"))
async def disconnect(app, message):
    m=await message.reply("Please wait..")   
    try:
        group     = await get_group(message.chat.id)
        user_id   = group["user_id"] 
        user_name = group["user_name"]
        verified  = group["verified"]
        channels  = group["channels"].copy()
    except :
        return await app.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
        return await m.edit(f"Only @{user_name} can use this command 😁")
    if bool(verified)==False:
        return await m.edit(f"Hey {message.from_user.mention} You Didn't Purchase Any Plan !\n Contact To My Owner @{OWNER}")    
    try:
        channel = int(message.command[-1])
        if channel not in channels:
            return await m.edit("You didn't added this channel yet Or Check Channel Id")
        channels.remove(channel)
    except:
        return await m.edit("❌ Incorrect format!\nUse `/remove ChannelID`")
    try:
        chat   = await app.get_chat(channel)
        group  = await app.get_chat(message.chat.id)
        c_link = chat.invite_link
        g_link = group.invite_link
        await yk.leave_chat(channel)
    except Exception as e:
        text = f"❌ Error: `{str(e)}`\nMake sure I'm admin in that channel & this group with all permissions and @{(user.username or user.mention)} is not banned there"
        return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Successfully removed from [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#DisConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await app.send_message(chat_id=LOG_CHANNEL, text=text)


@app.on_message(filters.group & filters.command("viewlist"))
async def connections(app, message):
    group = await get_group(message.chat.id)    
    user_id   = group["user_id"]
    user_name = group["user_name"]
    channels  = group["channels"]
    f_sub     = group["f_sub"]
    if message.from_user.id!=user_id:
        return await message.reply(f"Only @{user_name} can use this command 😁")
    if bool(channels)==False:
        return await message.reply("This group is currently not index to any channels!\nConnect one using /index")
    text = "This Group is currently indexed to:\n\n"
    for channel in channels:
        try:
            chat = await app.get_chat(channel)
            name = chat.title
            chat_nid = chat.id
            text += f"{name} : {chat_nid}\n"
        except Exception as e:
            await message.reply(f"❌ Error in `{channel}:`\n`{e}`", parse_mode=enums.ParseMode.MARKDOWN)
    if bool(f_sub):
        try:
            f_chat  = await app.get_chat(channel)
            f_title = f_chat.title
            f_link  = f_chat.invite_link
            text += f"\nFSub: [{f_title}]({f_link})"
        except Exception as e:
            await message.reply(f"❌ Error in FSub (`{f_sub}`)\n`{e}`",parse_mode=enums.ParseMode.MARKDOWN)
   
    await message.reply(text=text, disable_web_page_preview=True)