#     ____
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
import asyncio
import logging
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
    make_new_thread)
from beep_chatgpt import handle_message
from beep_price import find_style_code


load_dotenv()
nest_asyncio.apply()
logger = logging.getLogger(__name__)

intents = discord.Intents.all()
# intents.members = True
# intents.message_content = True
# intents.guilds = True
# intents.typing = True

bot = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")
TENOR_TOKEN = os.getenv("TENOR_TOKEN")
openai.api_key = os.getenv("OPEN_AI_TOKEN")
ip_token = os.getenv("IP_INFO_TOKEN")
home_channel = int(os.getenv("HOME"))
add_shoe_channel = int(os.getenv("ADD_SHOE"))

with open("user_agents.txt", "r") as ua:
    user_agents_list = ua.read().split('\n')
    headers_rotate = {'User-Agent': random.choice(user_agents_list)}
    print(headers_rotate)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
print(headers)


free_page = requests.get("https://free-proxy-list.net/",
                         headers=headers, timeout=1)
ssl_page = requests.get("http://www.sslproxies.org",
                        headers=headers, timeout=1)
new_proxies = BeautifulSoup(free_page.content, 'html.parser')
current_new_proxies = new_proxies.find(
    "textarea", {"class": "form-control"}).get_text()
new_ssl = BeautifulSoup(ssl_page.content, 'html.parser')
current_new_ssl = new_ssl.find(
    "textarea", {"class": "form-control"}).get_text()

modified_file_time = os.path.getmtime("valid_proxies.txt")
now_time = time.time()

startup_proxies(requests, time, random, now_time,
                modified_file_time, current_new_proxies, ip_token)


@bot.event
async def on_ready():
    '''boot the bot up'''
    print(f'{bot.user} has connected to Discord!')
    channel = discord.utils.get(bot.guilds[0].channels, name="home")
    # Set up logging for aiohttp
    aiohttp_logger = logging.getLogger('aiohttp.client')
    aiohttp_logger.setLevel(logging.WARNING)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=smooth+entrance&limit=10') as response:
            if response.status == 200:
                gifs_list = await response.json()
                gifs = gifs_list["data"]
                if gifs:
                    gif = random.choice(gifs)["url"]
                    await channel.send(gif)
                else:
                    logger.warning("No gifs")
            else:
                logger.error(f"Received {response.status}")
    await channel.send('''...
Type commands for list of commands

You can ask me questions about stuff and things
    but you must have punctuation! ( . ? !)
    ''')


@bot.event
async def on_member_join(member):
    '''when new member joins guild'''
    if member.id == bot.id:
        return
    channel = discord.utils.get(bot.guilds[0].channels, name="home")
    aiohttp_logger = logging.getLogger('aiohttp.client')
    aiohttp_logger.setLevel(logging.WARNING)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=Welcome&limit=10') as response:
            if response.status == 200:
                gifs_list = await response.json()
                gifs = gifs_list["data"]
                if gifs:
                    gif = random.choice(gifs)["url"]
                    await channel.send(gif)
                else:
                    logger.warning("No gifs")
            else:
                logger.error(f"Received {response.status}")
    channel = discord.utils.get(bot.guilds[0].channels, name="home")
    response = f"Welcome Welcome Welcome, {member.name}."
    await channel.send(response)


@bot.event
async def on_message(message):
    '''when member send a message in a channel'''

    if message.author == bot.user:
        return

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

                if where_msg == home_channel:
                    home_good = ("site list", "shoe list",
                                 "find style", "gimme", "help")
                    if where_msg == add_shoe_channel:
                        if any(message.content.startswith(good) for good in home_good):
                            await message.delete()
                            await channel.send("Dirty work in your thread please")
                        else:
                            addstr = "add"
                            if lowermsg.startswith(addstr):
                                await add_site(br_table_array,
                                               message,
                                               channel,
                                               cursor,
                                               branddb,
                                               br_list)

                            delete = "delete"
                            if lowermsg.startswith(delete):
                                await del_site(br_table_array,
                                               message,
                                               channel,
                                               cursor,
                                               branddb)
                            # refresh proxies
                            if "freshen up beep" in message.content.lower():
                                aiohttp_logger = logging.getLogger(
                                    'aiohttp.client')
                                aiohttp_logger.setLevel(logging.WARNING)
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=ill+be+back&limit=10') as response:
                                        if response.status == 200:
                                            gifs_list = await response.json()
                                            gifs = gifs_list["data"]
                                            if gifs:
                                                gif = random.choice(gifs)[
                                                    "url"]
                                                await channel.send(gif)
                                            else:
                                                logger.warning("No gifs")
                                        else:
                                            logger.error(
                                                f"Received {response.status}")
                                await fresh_while_on(aiofiles, current_new_proxies)
                                await check_while_on(aiofiles,
                                                     aiohttp,
                                                     asyncio,
                                                     random,
                                                     ip_token,
                                                     channel)

                if isinstance(channel, discord.Thread):
                    greets = ['hey beep', 'yo beep', 'ay beep',
                              'le beep', 'sir beep', 'hey boop',
                              'yo boop', 'ay boop', 'le boop', 'sir boop']
                    nanis = ["nani", "nani?", "nani?!"]

                    if "new thread" in lowermsg:
                        author = message.author
                        await make_new_thread(discord, bot, asyncio, message, check, channel, author)

                    # message responses
                    for greet in greets:
                        if greet.lower() in lowermsg:
                            aiohttp_logger = logging.getLogger(
                                'aiohttp.client')
                            aiohttp_logger.setLevel(logging.WARNING)
                            async with aiohttp.ClientSession() as session:
                                async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=yuh+sup&limit=10') as response:
                                    if response.status == 200:
                                        gifs_list = await response.json()
                                        gifs = gifs_list["data"]
                                        if gifs:
                                            gif = random.choice(gifs)["url"]
                                            await channel.send(gif)
                                        else:
                                            logger.warning("No gifs")
                                    else:
                                        logger.error(
                                            f"Received {response.status}")
                            await channel.send(f'Yuh sup @{message.author}')

                    for nani in nanis:
                        if nani.lower() in lowermsg or lowermsg[0] == "?":
                            aiohttp_logger = logging.getLogger(
                                'aiohttp.client')
                            aiohttp_logger.setLevel(logging.WARNING)
                            async with aiohttp.ClientSession() as session:
                                async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=nani&limit=10') as response:
                                    if response.status == 200:
                                        gifs_list = await response.json()
                                        gifs = gifs_list["data"]
                                        if gifs:
                                            gif = random.choice(gifs)["url"]
                                            await channel.send(gif)
                                        else:
                                            logger.warning("No gifs")
                                    else:
                                        logger.error(
                                            f"Received {response.status}")
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
                                              aiomysql,
                                              BeautifulSoup,
                                              asyncio,
                                              random,
                                              headers_rotate,
                                              message,
                                              home_channel,
                                              channel,
                                              cursor,
                                              branddb)

                    search = "gimme"
                    if lowermsg.startswith(search):
                        await search_shoes(aiohttp,
                                           random,
                                           GIPHY_TOKEN,
                                           lowermsg,
                                           cursor,
                                           branddb,
                                           channel)

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

                    if "help" in message.content.lower():
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
                Multi-link input only registers the
                sites coming from the first in the
                list. Seper■ate them with a , .

                https://www.n.com/no/win,
                www.f.com/af/shoe-09, www.g.com/e,
                http://www.flb.com/clo


            ***CHECK SHOE LIST
                Check all shoes list in the db by
                 sending "shoe list"


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
                    await handle_message(aiomysql, openai, message)

                # add shoe to db
                if message.channel.id == add_shoe_channel:
                    a_s_good = ("http", "www", "https", "got")
                    if where_msg == add_shoe_channel:
                        if not any(message.content.startswith(good) for good in a_s_good):
                            await message.delete()
                        else:
                            # adding shoes to db
                            await add_shoe(message,
                                           channel,
                                           cursor,
                                           branddb,
                                           br_table_array)


bot.run(TOKEN)
