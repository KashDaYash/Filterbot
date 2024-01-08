import asyncio
from time import time
import time 
from yash import app, yk
from yash.core.db import *
from config import *
from pyrogram import *
from pyrogram.errors import FloodWait
import urllib.parse
from yash import LOGGER

cmd = [
    "help", "id", "about", "check", "auth", "index", "remove", "viewlist",
    "leave", "log", "forcesub", "auto_del", "broadcast", "stats", "buy", "info", "about", "nofsub"
]
ignore_words = ["in", "and", "hindi", "movie", "tamil", "telugu", "dub", "hd", "man", "series", "full", "dubbed", "kannada", "season", "part", "all", "2022", "2021", "2023", "1", "2", "3", "4", "5", "6", "7" ,"8", "9", "0", "2020", "2019", "2018" , "2017", "2016", "2014", "all", "new", "2013", "()", "movies", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "1999", "1998", "1997", "1996", "1995", "-+:;!?*", "language", "480p", "720p", "1080p", "south", "Hollywood", "bollywood", "tollywood"]

async def should_ignore(word):
    return word.lower() in ignore_words

async def clean_query(query):
    words = query.split()
    cleaned_words = [word for word in words if not await should_ignore(word)]
    return " ".join(cleaned_words)

async def search_messages(channel, query):
    result_count = 0
    results = ""
    
    async for msg in yk.search_messages(chat_id=channel, query=query):
        name = (msg.text or msg.caption).split("\n")[0]
        if name in results:
            continue
        results += f"<b><i>♻️ {name}\n {msg.link}</i></b>\n\n"
        result_count += 1

        if result_count >= 8:
            break
    
    return results

@app.on_message(filters.text & filters.group & filters.incoming & ~filters.via_bot & ~filters.bot & ~filters.command(cmd))
async def search(bot, message):
    start_time = time.time()
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return
    data = await get_group(message.chat.id)
    if not data:
        return
    channels = data["channels"]
    if not channels:
        return
    if message.text.startswith("/"):
        return
    query = await clean_query(message.text)
    head = "<b>Here are the results</b>\n\n"
    results = ""
    
    try:
        # Search for the complete query first
        results += await search_messages(channels[0], query)
        
        # If less than 8 results, split the query and search
        if results.count("<b><i>") < 8:
            split_queries = query.split()
            for split_query in split_queries:
                results += await search_messages(channels[0], split_query)
                if results.count("<b><i>") >= 8:
                    break  # Break if 8 results are reached
        
        if not results:
            query_encoded = urllib.parse.quote_plus(query)
            no_results_message = f"No Results Found For <b>{query}</b>\n"
            msg = await message.reply_text(text=no_results_message, disable_web_page_preview=True, reply_markup=markup, parse_mode=enums.ParseMode.HTML)
            await asyncio.sleep(5)
            await msg.delete()
            return

        elapsed_time = time.time() - start_time
        footer = f"Searched in {elapsed_time:.2f} sec." # Add the duration to the footer
        msg = await message.reply_text(text=head + results + footer, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        _time = int(time()) + (2 * 60)
        await save_dlt_message(message.chat.id, _time, msg.id)
    except:
        pass