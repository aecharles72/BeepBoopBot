"""
Beep Boop Bot Main

"""
#    / __ )___  ___  ____
#   / __  / _ \/ _ \/ __ \
#  / /_/ /  __/  __/ /_/ /
# /_____/\___/\___/ .___/
#    / __ )____  /_/_  ____
#   / __  / __ \/ __ \/ __ \
#  / /_/ / /_/ / /_/ / /_/ /
# /_____/\____/\____/ .___/
#                  /_/
#                   _    _
#                  (_\__/(,_
#                  | \ `_////-._
#      _    _      L_/__ "=> __/`\
#     (_\__/(,_    |=====;__/___./
#     | \ `_////-._'-'-'-""""""`
#     J_/___"=> __/`\
#     |=====;__/___./
#     '-'-'-"""""""`
#
# @author: Andrew Charles

import os
import random
import time
import datetime
from datetime import timezone
import asyncio
import nest_asyncio
import aiohttp
import aiofiles
import aiomysql
import discord
import requests
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from bbbfunc import (
    startup_proxies,
    add_site,
    del_site,
    fresh_while_on,
    check_while_on,
    add_shoe,
    search_shoes,
    check,
    make_new_thread,
    beep_channels)
from beep_chatgpt import handle_message
from beep_price import find_style_code

# load env variables
load_dotenv()

# get nest async goin
nest_asyncio.apply()

intents = discord.Intents.all()
# intents.members = True
# intents.message_content = True
# intents.guilds = True
# intents.typing = True

# env variables
bot = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")
TENOR_TOKEN = os.getenv("TENOR_TOKEN")
openai.api_key = os.getenv("OPEN_AI_TOKEN")
ip_token = os.getenv("IP_INFO_TOKEN")
home_channel = int(os.getenv("HOME"))
add_shoe_channel = int(os.getenv("ADD_SHOE"))

# headers
with open("user_agents.txt", "r", encoding="utf-8") as ua:
    user_agents_list = ua.read().split('\n')
    headers_rotate = {'User-Agent': random.choice(user_agents_list)}
    print(headers_rotate)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
        like Gecko) Chrome/109.0.0.0 Safari/537.36'}
print(headers)

# proxy info
free_page = requests.get("https://free-proxy-list.net/",
                         headers=headers, timeout=1)
new_proxies = BeautifulSoup(free_page.content, 'html.parser')
current_new_proxies = new_proxies.find(
    "textarea", {"class": "form-control"}).get_text()

modified_file_time = os.path.getmtime("valid_proxies.txt")
now_time = time.time()

startup_proxies(requests, time, random, now_time,
                modified_file_time, current_new_proxies, ip_token)

# startup event  send gif and message, deletes itself after 10 seconds


@bot.event
async def on_ready():
    '''
    DESCRIPTION.
    boot the bot up

    Returns
    -------
    None.

    '''
    print(f'{bot.user} has connected to Discord!')
    channel = discord.utils.get(bot.guilds[0].channels, name="home")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=smooth+entrance&limit=10'
        ) as response:
            if response.status == 200:
                gifs_list = await response.json()
                gifs = gifs_list["data"]
                if gifs:
                    gif = random.choice(gifs)["url"]
                    send_gif = await channel.send(gif)
    send_mess = await channel.send('''...
Type commands for list of commands

You can ask me questions about stuff and things
    but you must have punctuation! ( . ? !)
    ''')
    await send_gif.delete(delay=10)
    await send_mess.delete(delay=10)


@bot.event
async def on_member_join(member):
    '''


    Parameters
    ----------
    member : TYPE
        DESCRIPTION.
        when new member joins guild

    Returns
    -------
    None.

    '''

    if member.id == bot.user.id:
        return
    channel = bot.get_channel(home_channel)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=Welcome&limit=10'
        ) as response:
            if response.status == 200:
                gifs_list = await response.json()
                gifs = gifs_list["data"]
                if gifs:
                    gif = random.choice(gifs)["url"]
                    await channel.send(gif)
    channel = discord.utils.get(bot.guilds[0].channels, name="home")
    response = f"Welcome Welcome Welcome, {member.name}."
    await channel.send(response)


@bot.event
async def on_raw_reaction_add(payload):
    '''


    Parameters
    ----------
    payload : TYPE
        DESCRIPTION.
        triggers when any emote is added

    Returns
    -------
    None.

    '''

    print("RAW: EMO: 1")
    message_id = payload.message_id
    print(f"RAW EMO: {message_id}")
    pay_channel = payload.channel_id
    channel = bot.get_channel(pay_channel)
    message = await channel.fetch_message(message_id)
    print(f"RAW EMO: {channel}")
    member = payload.member
    print(f"RAW EMO: {member}")
    # embeds = payload.message.embeds
    click_emoji = payload.emoji
    # if user.id != payload.message.author.id:
    print("RAW EMO: 2")
    async with aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='shoe_brands'
    ) as shoe_db:
        async with shoe_db.acquire() as branddb:
            async with branddb.cursor() as cursor:
                await cursor.execute("SELECT site_url FROM shoe_sites")
                br_table = await cursor.fetchall()
                br_table_array = [a for b in br_table for a in b]
                br_list = '\n'.join(br_table_array)
                now_datetime = datetime.datetime.now(timezone.utc)
                now_datetime_s = now_datetime.timestamp()
                mess_create = message.created_at
                mess_create_s = mess_create.timestamp()
                time_diff = (now_datetime_s - mess_create_s)
                print(f"RAW EMO: {message.created_at}")
                print(f"RAW EMO: {now_datetime}")
                print(f"RAW EMO: {time_diff}")
                if time_diff <= 12:
                    print("RAW EMO: less")
                    return
                print("RAW EMO: 3")
                if click_emoji == discord.PartialEmoji(name='👀'):
                    send_list = await channel.send(br_list)
                    await send_list.delete(delay=15)
                    return
                print("RAW EMO: 4")
                if click_emoji == discord.PartialEmoji(name='👟'):
                    s_h = ("SELECT name FROM shoes")
                    await cursor.execute(s_h)
                    shoe_table = await cursor.fetchall()
                    shoe_table_array = [a for b in shoe_table for a in b]
                    shoe_list = '\n'.join(shoe_table_array)
                    send_shoe = await channel.send(shoe_list)
                    await send_shoe.delete(delay=30)
                    return
                print("RAW EMO: 5")
                if click_emoji == discord.PartialEmoji(name='💵'):
                    style_send = await channel.send('''*
    ***CHECK CURRENT PRICE
        Check for current prices in db by
         sending "find style" followed by
         the style code.One code at a time
    
        e.) find style CHJKS-9878''')
                    await style_send.delete(delay=30)
                print("RAW EMO: 6")
                if click_emoji == discord.PartialEmoji(name='📚'):
                    add_send = await channel.send(
                        '<https://discord.com/channels/1069760567692230676/1076734799823257624>')
                    await channel.send('''*
    ***ADD SHOE TO DB
        Click the link below
        then send the link of the item.
        As long as the site is in site 
        list you str8!''')
                    await add_send.delete(delay=10)

                print("RAW EMO: 7")
                if click_emoji == discord.PartialEmoji(name='🔍'):
                    gimme_send = await channel.send('''*
    ***SEARCH DB
        Search for shoes in database by
        sending "gimme" followed by 
        search words
        
            type gimme KEYWORD''')
                    await gimme_send.delete(delay=10)

                print("RAW EMO: 8")
                if click_emoji == discord.PartialEmoji(name='👍🏾'):
                    add_site_send = await channel.send('''*
    ***ADD SITE TO DB
        Send "add" then the site followed
         by the appropriate format letter.

        a, b, c, or d. "www.store.com a"

        Format A
        .com/blah/n-a-m-e/scORsku

        Format B
        .com/blah/n-a-m-e-sc-sc

        Format C
        dont work

        Format D
        .com/blah/n-a-m-e-sc''')
                    await add_site_send.delete(delay=20)

                print("RAW EMO: 9")
                if click_emoji == discord.PartialEmoji(name='👎🏾'):
                    del_site_send = await channel.send('''*
    ***DELETE SITE IN DB
        Send "delete" then the site''')
                    await del_site_send.delete(delay=20)

                print("RAW EMO: 10")
                if click_emoji == discord.PartialEmoji(name='🌪️'):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=ill+be+back&limit=10'
                        ) as response:
                            if response.status == 200:
                                gifs_list = await response.json()
                                gifs = gifs_list["data"]
                                if gifs:
                                    gif = random.choice(gifs)[
                                        "url"]
                                    gif_send = await channel.send(gif)
                                    await gif_send.delete(delay=60)
                    to_home = discord.utils.get(
                        bot.guilds[0].channels, name="home")
                    send_home = await to_home.send(f"{member} refreshing proxies")
                    await send_home.delete(delay=60)
                    await fresh_while_on(aiofiles, current_new_proxies)
                    await check_while_on(aiofiles,
                                         aiohttp,
                                         asyncio,
                                         ip_token,
                                         channel)
                    await gimme_send.delete(delay=10)

                print("RAW EMO: 12")
                if click_emoji == discord.PartialEmoji(name='🧹'):  # PURGE THREAD
                    await channel.purge(after=mess_create)

                print("RAW EMO: 13")
                if click_emoji == discord.PartialEmoji(name='🤬'):
                    com_send = await channel.send('''*
    **********************>
    ****COMMANDS..........>
    ****..................>
    ****site list.........>
    ****shoe list.........>
    ****find style........>
    ****add...............>
    ****delete............>
    ****gimme.............>
    ****freshen up beep>..>
    ****help..............>
    ****..................>
    **********************>''')
                    await com_send.delete(delay=30)
                print("RAW EMO: 14")
                if click_emoji == discord.PartialEmoji(name='❓'):
                    help_send = await channel.send('''*
    ***ADD SHOE TO DB
        Send link to add shoe! As long as
         the site is in site list you str8!
    
    
    ***CHECK SITE LIST
        Check the site list by sending
         "site list". No site in list?
    
    
    ***AD SITE TO DB
        Send "add" then the site followed
         by the appropriate format letter.
    
        a, b, c, or d. "www.store.com a"
    
        *Don't worry about
        the rest(?=>) part of the url*
    
    
        Format A
        .com/blah/n-a-m-e/scORsku
    
        Format B
        .com/blah/n-a-m-e-sc-sc
    
        Format C
        dont work
    
        Format D
        .com/blah/n-a-m-e-sc
    
    
    ***ADDING MULTIPLE ITEMS
        Multi-link input needs to be seperated
        by a comma with no spaces
    
        https://www.n.com/no/win,www.f.com/af/shoe-09,www.g.com/e,
    
    ***CHECK SHOE LIST
        Check all shoes list in the db by
         sending "shoe list"|
    
    
    ***CHECK CURRENT PRICE
        Check for current prices in db by
         sending "find style" followed by
         the style code.One code at a time
    
        find style CHJKS-9878
    
    
    ***REFRESH PROXIES
        Refresh the proxies by sending
        "freshen up beep"
    
    
    ***SEARCH DB
        Search for shoes in database by
        sending "gimme" followed by search
        words''')
                    await help_send.delete(delay=30)

# when a message is sent in the discord channel


@bot.event
async def on_message(message):
    '''


    Parameters
    ----------
    message : TYPE v
        DESCRIPTION.
        when member send a message in a channel

    Returns
    -------
    None.

    '''

    # prevent bot replying to bot
    if message.author == bot.user:
        return

    # get channel info of guild
    await beep_channels(discord, aiomysql, message)

    # connect to shoe brands db asynchronously
    async with aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='shoe_brands'
    ) as shoe_db:
        async with shoe_db.acquire() as branddb:
            async with branddb.cursor() as cursor:
                await cursor.execute("SELECT site_url FROM shoe_sites")
                br_table = await cursor.fetchall()
                br_table_array = [a for b in br_table for a in b]
                br_list = '\n'.join(br_table_array)
                channel = message.channel
                lowermsg = message.content.lower()
                where_msg = message.channel.id

                purge = 'beep clean'
                if lowermsg.startswith(purge):
                    await channel.purge()

                # only messages sent in home
                if where_msg == home_channel:
                    home_good = ("site list", "shoe list",
                                 "find style", "gimme", "help")
                    if any(message.content.startswith(good) for good in home_good):
                        await message.delete()
                        await channel.send("Dirty work in your thread please")
                    else:
                        # add new site
                        addstr = "add"
                        if lowermsg.startswith(addstr):
                            await add_site(br_table_array,
                                           message,
                                           channel,
                                           cursor,
                                           branddb,
                                           br_list)
                        # delete site
                        delete = "delete"
                        if lowermsg.startswith(delete):
                            await del_site(message,
                                           channel,
                                           cursor,
                                           branddb)
                        # refresh proxies
                        if "freshen up beep" == message.content.lower():
                            async with aiohttp.ClientSession() as session:
                                async with session.get(
                                    f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=ill+be+back&limit=10'
                                ) as response:
                                    if response.status == 200:
                                        gifs_list = await response.json()
                                        gifs = gifs_list["data"]
                                        if gifs:
                                            gif = random.choice(gifs)[
                                                "url"]
                                            await channel.send(gif)
                            await fresh_while_on(aiofiles, current_new_proxies)
                            await check_while_on(aiofiles,
                                                 aiohttp,
                                                 asyncio,
                                                 ip_token,
                                                 channel)

                        # create a new thread
                        if "new thread" == lowermsg:
                            author = message.author
                            await make_new_thread(aiomysql, discord, bot, asyncio, message, check, channel, author)

                # only messages sent in threads
                if isinstance(channel, discord.Thread):
                    greets = ['hey beep', 'yo beep', 'ay beep',
                              'le beep', 'sir beep', 'hey boop',
                              'yo boop', 'ay boop', 'le boop', 'sir boop']
                    nanis = ["nani", "nani?", "nani?!"]

                    # message responses
                    for greet in greets:
                        if greet.lower() in lowermsg:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(
                                    f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=yuh+sup&limit=10'
                                ) as response:
                                    if response.status == 200:
                                        gifs_list = await response.json()
                                        gifs = gifs_list["data"]
                                        if gifs:
                                            gif = random.choice(gifs)["url"]
                                            await channel.send(gif)
                            await channel.send(f'Yuh sup @{message.author}')

                    for nani in nanis:
                        if nani.lower() in lowermsg or lowermsg[0] == "?":
                            async with aiohttp.ClientSession() as session:
                                async with session.get(
                                    f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=nani&limit=10'
                                ) as response:
                                    if response.status == 200:
                                        gifs_list = await response.json()
                                        gifs = gifs_list["data"]
                                        if gifs:
                                            gif = random.choice(gifs)["url"]
                                            await channel.send(gif)
                            await channel.send("Nani?!")

                    # get site list
                    give_site_list = "site list"
                    if give_site_list in lowermsg:
                        await channel.send(br_list)
                        return

                    # get shoe list
                    give_shoe_list = "shoe list"
                    if give_shoe_list in lowermsg:
                        # change brand to model
                        s_h = ("SELECT name FROM shoes")
                        await cursor.execute(s_h)
                        shoe_table = await cursor.fetchall()
                        shoe_table_array = [a for b in shoe_table for a in b]
                        shoe_list = '\n'.join(shoe_table_array)
                        await channel.send(shoe_list)
                        return

                    # input find style (style code)
                    find_by_style_code = "find style"
                    if lowermsg.startswith(find_by_style_code):
                        await find_style_code(aiohttp,
                                              BeautifulSoup,
                                              asyncio,
                                              random,
                                              headers_rotate,
                                              message,
                                              home_channel,
                                              channel,
                                              cursor,
                                              branddb)
                    # search shoe db
                    search = "gimme"
                    if lowermsg.startswith(search):
                        await search_shoes(aiohttp,
                                           random,
                                           GIPHY_TOKEN,
                                           lowermsg,
                                           cursor,
                                           channel)
                    # get commands
                    if "commands" in lowermsg:
                        await channel.send('''*
            **********************>
            ****COMMANDS..........>
            ****..................>
            ****site list.........>
            ****shoe list.........>
            ****find style........>
            ****add...............>
            ****delete............>
            ****gimme.............>
            ****freshen up beep>..>
            ****help..............>
            ****..................>
            **********************>''')

                    # get help
                    if lowermsg == "help":
                        await channel.send('''*
***ADD SHOE TO DB
    Send link to add shoe! As long as
     the site is in site list you str8!


***CHECK SITE LIST
    Check the site list by sending
     "site list". No site in list?


***AD SITE TO DB
    Send "add" then the site followed
     by the appropriate format letter.

    a, b, c, or d. "www.store.com a"

    Format A
    .com/blah/n-a-m-e/scORsku

    Format B
    .com/blah/n-a-m-e-sc-sc

    Format C
    dont work

    Format D
    .com/blah/n-a-m-e-sc


***ADDING MULTIPLE ITEMS
    Multi-link input needs to be seperated
    by a comma with no spaces

    https://www.n.com/no/win,www.f.com/af/shoe-09,www.g.com/e,

***CHECK SHOE LIST
    Check all shoes list in the db by
     sending "shoe list"|


***CHECK CURRENT PRICE
    Check for current prices in db by
     sending "find style" followed by
     the style code.One code at a time

    find style CHJKS-9878


***REFRESH PROXIES
    Refresh the proxies by sending
    "freshen up beep"


***SEARCH DB
    Search for shoes in database by
    sending "gimme" followed by search
    words''')

                ###BEEPAI###
                if isinstance(channel, discord.Thread) and not channel.id == home_channel:
                    await handle_message(aiomysql, openai, message, channel)

                # add shoe to db
                print(f"ADDSHO: {message.channel.id}")
                print(f"ADDSHO: E{add_shoe_channel}")
                if message.channel.id == add_shoe_channel:
                    print("ADDSHOE: shoe1")
                    a_s_good = ("http", "www", "https", "got")
                    if where_msg == add_shoe_channel:
                        print("ADDSHOE: 2")
                        if not any(message.content.startswith(good) for good in a_s_good):
                            await message.delete()
                        else:
                            # adding shoes to db
                            await add_shoe(message,
                                           channel,
                                           cursor,
                                           branddb,
                                           br_table_array)


@bot.event
async def on_raw_thread_delete(payload):
    '''
    Parameters
    ----------
    payload : TYPE dict
        DESCRIPTION.
        rename channel when deleted

    Returns
    -------
    None.

    '''
    channel_id = payload.thread.id
    print(f"THRDEL: {channel_id} deleted")
    date_time = datetime.datetime.now(timezone.utc)
    thread_name = payload.thread.name
    print(f"THRDEL: {thread_name} deleted")
    async with aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='beep_ai'
    ) as beep_ch:
        async with beep_ch.acquire() as beep_chan:
            async with beep_chan.cursor() as beep_chan_cursor:
                is_it = f"SELECT thread_name FROM beep_channels WHERE thread_name = '{thread_name}'"
                await beep_chan_cursor.execute(is_it)
                it_is = await beep_chan_cursor.fetchone()
                if it_is is None:
                    return
                arch_channel = "UPDATE beep_channels SET thread_name = '{}' WHERE thread_id = '{}'"
                arch_channel = arch_channel.format(
                    thread_name + " DELETED " + str(date_time), channel_id)
                print(f"THRDEL: {arch_channel}")
                await beep_chan_cursor.execute(arch_channel)
                await beep_chan.commit()

bot.run(TOKEN)
