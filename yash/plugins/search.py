import asyncio
from time import time
from cachetools import TTLCache
from yash import app, yk
from yash.core.db import *
from config import *
from pyrogram import *
from pyrogram.errors import FloodWait

MESSAGE_LENGTH = 4096

ignore_words = ["in", "and", "hindi", "movie", "tamil", "telugu", "dub", "hd", "man", "series", "full", "dubbed", "kannada", "season", "part", "all", "2022", "2021", "2023", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "2020", "2019", "2018", "2017", "2016", "2014", "all", "new", "2013", "()", "movies", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "1999", "1998", "1997", "1996", "1995", "-+:;!?*", "language", "480p", "720p", "1080p", "south", "Hollywood", "bollywood", "tollywood",]

async def should_ignore(word):
    return word.lower() in ignore_words

async def clean_query(query):
    words = query.split()
    cleaned_words = [word for word in words if not await should_ignore(word)]
    return " ".join(cleaned_words)

cache = TTLCache(maxsize=100, ttl=300)

async def search_messages(chat_id, query):
    cache_key = f"{chat_id}:{query}"
    cached_results = cache.get(cache_key)
    
    if cached_results:
        return cached_results

    try:
        results = ""
        messages = []

        async for msg in yk.search_messages(int(chat_id), query=query, limit=8):
            messages.append(msg)

        for msg in messages:
            if msg.caption or msg.text:
                full_sentence = msg.text or msg.caption
                if query.lower() in full_sentence.lower():
                    name = full_sentence.split("\n")[0]
                    result_entry = f"{name}\n {msg.link}\n\n"
                    results += result_entry

                    if len(results) >= 8:
                        break

        cache[cache_key] = results
        return results
    except Exception as e:
        print(f"Error searching messages: {str(e)}")
        return ""

async def search_channel_chunk(channels, query):
    max_results = 6
    results = []
    added_results = set()

    tasks = [search_messages(chat_id, query) for chat_id in channels]

    search_results = await asyncio.gather(*tasks)

    for result in search_results:
        if result and result not in added_results:
            added_results.add(result)
            results.append(result)

            if len(results) >= max_results:
                break

    return results

@app.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["auth", "index", "id", "autodel"]))
async def search(app, message):
    star = time()
    f_sub = await force_sub(app, message)
    if f_sub == False:
        return
    veri = await get_group(message.chat.id)
    verified = veri["verified"]
    if verified == False:
        return
    channels = veri['channels']
    if not channels:
        return
    if message.text.startswith("/"):
        return
    query = await clean_query(message.text)
    query_words = query.split()
    max_results = 6
    results = []
    added_results = set()

    chunk_size = 5
    channel_chunks = [channels[i:i + chunk_size] for i in range(0, len(channels), chunk_size)]
    tasks = []

    for chunk in channel_chunks:
        tasks.append(search_channel_chunk(chunk, query))
    chunked_results = await asyncio.gather(*tasks)
    chunked_results = [result for chunk_results in chunked_results for result in chunk_results]

    for result in chunked_results:
        if result and result not in added_results:
            added_results.add(result)
            results.append(result)

            if len(results) >= max_results:
                break

    if results:
        end = time()
        time_elapsed = end - star
        combined_results = "".join(results)
        msg = await message.reply(f"Here are the results 👇 \n{combined_results} Result Searched in {time_elapsed:.2f} sec", disable_web_page_preview=True)
        _time = int(time()) + (1 * 60)

        try:
            message_id = msg.id

            if veri['auto_del'] == True:
                await save_dlt_message(message.chat.id, _time, message_id)
                
        except FloodWait as e:
            print(e)
    else:
        xx = await message.reply("No Results Found 🔍")
        await asyncio.sleep(20)
        await xx.delete()