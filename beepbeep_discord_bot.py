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
import json
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
    check,
    search_shoes,
    make_new_thread,
    beep_channels,
    update_url_imgs,
    # tup_to_str,
    tup_to_str_list,
    msg_gif,
    tup_to_list,
    get_em)
from beep_chatgpt import handle_message
from beep_price import find_style_code, update_nike

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
with open("user_agents.txt", "r") as ua:
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
    string = "smooth+entrance"
    await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)

    send_mess = await channel.send('''...
Type commands for list of commands

You can ask me questions about stuff and things
    but you must have punctuation! ( . ? !)
    ''')

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

    member.add_roles()

    channel = bot.get_channel(home_channel)
    string = "welcome"
    await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)
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
                br_list = await tup_to_str_list(br_table)
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
                print("RAW EMO: WELCOMEWALL")
                if click_emoji == discord.PartialEmoji(name='🍥'):
                    member_role = discord.utils.get(bot.guilds[0].roles, name="User")
                    await member.add_roles(member_role)
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
                    print(shoe_table)
                    shoe_list = await tup_to_list(shoe_table)
                    print(shoe_list)
                    # embed = discord.Embed(title="Shoe List", description='\n'.join(shoe_list))
                    max_items_per_embed = 100
                    total_embeds = (len(shoe_list) // max_items_per_embed) + 1
                    print(total_embeds)
                    for i in range(total_embeds):
                        embed = discord.Embed(title="List", description="")
                        start_index = i * max_items_per_embed
                        end_index = min(start_index + max_items_per_embed, len(shoe_list))
                        for item in shoe_list[start_index:end_index]:
                            embed.description += f"- {item}\n"
                        if i == 0:
                            print("1")
                            message = await channel.send(embed=embed)
                            await message.delete(delay=30)
                        else:
                            print("2")
                            embed_more = await channel.send(embed=embed)
                            await embed_more.delete(delay=30)
                    # print("3")
                    # send_shoe = await channel.send(embed=embed)
                    # await send_shoe.delete(delay=30)
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
                    string = "I'll+be+back"
                    await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)
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

                print("RAW EMO: 12")
                if click_emoji == discord.PartialEmoji(name='🧹'):  # PURGE THREAD
                    await channel.purge(after=mess_create)

                print("RAW : ")
                if click_emoji == discord.PartialEmoji(name='📥'):
                    with open("scoop_list.txt", "r", encoding="utf-8") as s_l:
                        for url in s_l:
                            await get_em(aiohttp, asyncio, BeautifulSoup, bot, channel, add_shoe_channel, url)
                            asyncio.sleep(1)

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
                br_table_array = await tup_to_list(br_table)
                br_list = await tup_to_str_list(br_table)
                channel = message.channel
                lowermsg = message.content.lower()
                where_msg = message.channel.id

                clear = 'beep clean'
                if lowermsg.startswith(clear):
                    async for message in channel.history():
                        if not message.pinned:
                            await message.delete()
                            await asyncio.sleep(0.75)

                purge = "beep destroy"
                if lowermsg.startswith(purge):
                    await message.channel.purge()
                    await message.channel.send("You asked for it")

                # only messages sent in home
                if where_msg == home_channel:

                    # prevent bot replying to bot
                    if message.author == bot.user:
                        return

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
                            string = "I'll+be+back"
                            await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)
                            await fresh_while_on(aiofiles, current_new_proxies)
                            await check_while_on(aiofiles,
                                                 aiohttp,
                                                 asyncio,
                                                 ip_token,
                                                 channel)

                        # create a new thread
                        if "new thread" == lowermsg:
                            author = message.author
                            await make_new_thread(aiomysql,
                                                  discord,
                                                  bot,
                                                  asyncio,
                                                  message,
                                                  check,
                                                  channel,
                                                  author)

                        if "beep look" == lowermsg:
                            await update_url_imgs(aiohttp,
                                                  BeautifulSoup,
                                                  headers,
                                                  branddb,
                                                  channel,
                                                  cursor,
                                                  message)

                        gettem = "gettem"
                        if lowermsg.startswith(gettem):
                            if "www.nike.com" in lowermsg:
                                url = message.content.split()
                                url = url[1]
                                print(url)
                                shoe_channel = bot.get_channel(add_shoe_channel)
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(url) as resp:
                                        html = await resp.text()
                                        soup = BeautifulSoup(html, 'html.parser')
                                        links = []
                                        for link in soup.find_all('a'):
                                            href = link.get('href')
                                            if href and href.startswith('http') and ".com/t/" in href:
                                                links.append(href)
                                                await shoe_channel.send(href)
                                                await asyncio.sleep(1)
                                        await channel.send("Done")

                        all_nike = "update nike"
                        if lowermsg == all_nike:
                            all_nike_urls = "SELECT url FROM shoes"
                            await cursor.execute(all_nike_urls)
                            nike_fetch = await cursor.fetchall()
                            all_nike_links_list = await tup_to_list(nike_fetch)
                            nike_urls = []
                            for url in all_nike_links_list:
                                if "www.nike.com" in url:
                                    nike_urls.append(url)
                            print(nike_urls)
                            await update_nike(aiohttp, asyncio, BeautifulSoup, json, random, branddb, cursor, channel, nike_urls)

                # only messages sent in threads
                if isinstance(channel, discord.Thread):

                    # prevent bot replying to bot
                    if message.author == bot.user:
                        return

                    greets = ['hey beep', 'yo beep', 'ay beep',
                              'le beep', 'sir beep', 'hey boop',
                              'yo boop', 'ay boop', 'le boop', 'sir boop']
                    nanis = ["nani", "nani?", "nani?!"]

                    # message responses
                    for greet in greets:
                        if greet.lower() in lowermsg:
                            string = "yuh+sup"
                            await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)
                            await channel.send(f'Yuh sup @{message.author}')

                    for nani in nanis:
                        if nani.lower() in lowermsg or lowermsg[0] == "?":
                            string = "nani"
                            await msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string)
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
                        shoe_list = await tup_to_str_list(shoe_table)
                        await channel.send(shoe_list)
                        return

                    # input find style (style code)
                    find_by_style_code = "find style"
                    if lowermsg.startswith(find_by_style_code):
                        await find_style_code(aiohttp,
                                              discord,
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
                    give = "gimme"
                    if lowermsg.startswith(give):
                        await search_shoes(discord,
                                           aiohttp,
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
    get_role = discord.utils.get(bot.guilds[0].roles, name=thread_name)
    print(f"THRDEL: {get_role}")
    await get_role.delete()
    print("THRDEL: deleted")
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
