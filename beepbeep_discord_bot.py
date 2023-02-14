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


'''queue the proxies'''
# import queue
import aiohttp
import aiofiles
import aiomysql
# import threading
import discord
import os
import requests
import random
import time
import pymysql
import asyncio
import nest_asyncio
import logging
import openai
from bs4 import BeautifulSoup
# from check_proxies import (fresh_proxies, check_proxies )
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()
logger = logging.getLogger(__name__)

intents = discord.Intents.all()  # or .all() if you ticked all, that is easier
intents.members = True  # If you ticked the SERVER MEMBERS INTENT
intents.message_content = True
intents.guilds = True
intents.typing = True
bot = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")
TENOR_TOKEN = os.getenv("TENOR_TOKEN")
openai.api_key = os.getenv("OPEN_AI_TOKEN")
ip_token = os.getenv("IP_INFO_TOKEN")

branddb = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='shoe_brands')

with open("user_agents.txt", "r") as ua:
    user_agents_list = ua.read().split('\n')
    headers_rotate = {'User-Agent': random.choice(user_agents_list)}
    print(headers_rotate)
    ua.close()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
print(headers)

# q= queue.Queue()
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


def startup_proxies():
    if now_time - modified_file_time > 540:
        with open("proxy_list.txt", "w") as pl:
            print(now_time)
            print(modified_file_time)
            fresh_proxie = current_new_proxies[75:]
            # fresh_ssl = current_new_ssl[75:]
            pl.write(fresh_proxie)
            # await pl.write(fresh_ssl)
            print("Done adding fresh proxies")
            pl.close()
        with open("proxy_list.txt", "r") as f:
            proxies = f.read().split("\n")
            valid_proxies = []
            for proxy in proxies:
                check_p = proxy.split(":").pop(0)
                checker = f"https://ipinfo.io/{check_p}/json?token={ip_token}"
                print(proxy)
                with requests.get(checker) as res:
                    print(checker)
                    print(res.status_code)
                    if res.status_code == 200:
                        print(proxy)
                        valid_proxies.append(proxy)
                    else:
                        time.sleep(random.uniform(1, 5))
                    if res.status_code == 429:
                        break
                f.close()

        with open("valid_proxies.txt", "w") as v:
            v.write("\n".join(valid_proxies))
            print("done check")
            v.close()


startup_proxies()


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
    await channel.send('''
    Good to go
    Type help for help
    Type commands for list of commands
    Type freshen up beep to refresh proxies.
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

    channel = message.channel
    lowermsg = message.content.lower()
    greets = ['hey beep', 'yo beep', 'ay beep',
              'le beep', 'sir beep', 'hey boop',
              'yo boop', 'ay boop', 'le boop', 'sir boop']
    nanis = ["nani", "nani?", "nani?!"]
    searchs = ['check price', 'current price']
    prefixes = ("http", "Http", "www", "WWW")

    cursor = branddb.cursor()
    cursor.execute("SELECT site_url FROM shoe_sites")
    br_table = cursor.fetchall()
    br_table_array = [a for b in br_table for a in b]
    br_list = '\n'.join(br_table_array)

    # message responses
    for greet in greets:
        if greet.lower() in lowermsg:
            aiohttp_logger = logging.getLogger('aiohttp.client')
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
                        logger.error(f"Received {response.status}")
            await channel.send(f'Yuh sup @{message.author}')

    for nani in nanis:
        if nani.lower() in lowermsg or lowermsg[0] == "?":
            aiohttp_logger = logging.getLogger('aiohttp.client')
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
                        logger.error(f"Received {response.status}")
            await channel.send("Nani?!")

    for search in searchs:
        if search.lower() in lowermsg:
            aiohttp_logger = logging.getLogger('aiohttp.client')
            aiohttp_logger.setLevel(logging.WARNING)
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=search&limit=10') as response:
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
            await channel.send('Chu lookin for? Type gimme first')

    # add site to site list
    async def add_site():
        breakdown = message.content.split()
        for site in breakdown:
            if breakdown[1] in br_table_array:
                await channel.send('already there man')
                return
            else:
                insert_site = (
                    f"INSERT INTO shoe_sites (site_url, site_group) VALUE ('{breakdown[1]}','{breakdown[2].upper()}');")
                cursor.execute(insert_site)
                branddb.commit()
                cursor.close()
                await channel.send("added")
                await channel.send(f"...\nAdded {breakdown[1].upper()} to group {breakdown[2].upper()} in list:\n{br_list}")
                return

    addstr = "add"
    if lowermsg.startswith(addstr):
        await add_site()

    # get site list
    give_site_list = "site list"
    if give_site_list in lowermsg:
        await channel.send(br_list)
        return

    # get shoe list
    give_shoe_list = "shoe list"
    if give_shoe_list in lowermsg:
        sh = ("SELECT name FROM shoes")  # change brand to model
        cursor.execute(sh)
        shoe_table = cursor.fetchall()
        shoe_table_array = [a for b in shoe_table for a in b]
        shoe_list = '\n'.join(shoe_table_array)
        await channel.send(shoe_list)
        return

    async def fresh_while_on():
        async with aiofiles.open("proxy_list.txt", "w") as pl:
            fresh_proxies = current_new_proxies[75:]
            await pl.write(fresh_proxies)
            print("Done adding fresh proxies")
            await pl.close()

    async def check_while_on():
        '''make sure the proxies are working'''
        valid_proxies = []
        print("Begin Check")
        async with aiofiles.open("proxy_list.txt", "r") as f:
            proxies = ''.join(await f.read()).split()
            valid_proxies = []
            async with aiohttp.ClientSession() as session:

                for proxy in proxies:
                    check_p = proxy.split(":").pop(0)
                    checker = f"https://ipinfo.io/{check_p}/json?token={ip_token}"
                    print(proxy)
                    async with session.get(checker) as res:
                        print(res.status)
                        if res.status == 200:
                            valid_proxies.append(proxy)
                            await asyncio.sleep(random.uniform(1, 5))
                        else:
                            await asyncio.sleep(random.uniform(1, 5))
                        if await res.status == 429:
                            await channel.send("429 DEAD")
                            break
            async with aiofiles.open("valid_proxies.txt", "w") as v:
                await v.write("\n".join(valid_proxies))

    # refresh proxies
    if "freshen up beep" in message.content.lower():
        aiohttp_logger = logging.getLogger('aiohttp.client')
        aiohttp_logger.setLevel(logging.WARNING)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=ill+be+back&limit=10') as response:
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
        await fresh_while_on()
        await check_while_on()

    # input find style (style code)
    async def find_style_code():
        if message.channel.id == 1074057921400414319:
            strip_mess = message.content[10:].strip().split(",")
            style_c = ("SELECT style_code FROM shoes")
            cursor.execute(style_c)
            style_code_table_array = [a for b in cursor.fetchall() for a in b]
            for scode in strip_mess:
                # message_length = len(message.content[10:].split(","))
                if scode in style_code_table_array:
                    # shoe = ("SELECT name FROM shoes WHERE style_code = %s") #change brand to model
                    # cursor.execute(shoe, (scode))
                    # shoe_sc_found = cursor.fetchall()
                    sc_urls = ("SELECT url FROM shoes WHERE style_code = %s")
                    cursor.execute(sc_urls, (scode))
                    # URL = ', '.join(sc_url_list)
                    sc_url_list = []
                    sc_url_list.extend(
                        [a for b in cursor.fetchall() for a in b])
                    sc_url_list_length = len(sc_url_list)
                    # shoe_sc = [a for b in shoe_sc_found for a in b]
                    # shoe_code_list = '\n'.join(shoe_sc.replace("-", " "))
                    await channel.send(sc_url_list)
                    for s in sc_url_list:
                        await channel.send(s)
                        try:
                            success = False
                            if "www.nike.com" in s.lower():
                                await channel.send(scode + " it nike")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        # try:
                                        print(
                                            f"using the proxy: {proxy.strip()}")
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(s) as response:
                                                print(response)
                                                print(response.status)
                                                if response.status == 200:
                                                    success = True
                                                    soup = BeautifulSoup(
                                                        await response.text(),
                                                        "html.parser")
                                                    nike_current_price = soup.find(
                                                        "div", {
                                                            "class": "product-price css-11s12ax is--current-price css-tpaepq"
                                                        }).get_text()
                                                    insert_query = f"UPDATE shoes SET price = '{nike_current_price}' WHERE url = '{s}'"
                                                    cursor.execute(
                                                        insert_query)
                                                    branddb.commit()
                                                    await channel.send(nike_current_price)
                                                    await channel.send(s)
                                                else:
                                                    print(response.status)
                                                    print("damn")
                                                    await asyncio.sleep(random.uniform(1, 5))
                                                    continue
                                    # except:
                                        # print("damn")
                                        # await asyncio.sleep(random.uniform(1, 5))
                                        # continue
                                    # finally:
                                                if success == True:
                                                    break

                            elif "www.footlocker.com" in s.lower():
                                await channel.send(scode + " it footlocker")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        # try:
                                        print(
                                            f"using the proxy: {proxy.strip()}")
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(s) as response:
                                                print(response)
                                                print(response.status)
                                                if response.status == 200:
                                                    success = True
                                                    soup = BeautifulSoup(
                                                        await response.content, 'html.parser')
                                                    fl_current_price = soup.find(
                                                        "span", {"class": "ProductPrice"}).get_text()
                                                    insert_query = (
                                                        f"UPDATE shoes SET price = '{fl_current_price}' WHERE url = '{s}';")
                                                    cursor.execute(
                                                        insert_query)
                                                    branddb.commit()
                                                    await channel.send(fl_current_price)
                                                    await channel.send(s)
                                                else:
                                                    print(response.status)
                                                    print("damn")
                                                    await asyncio.sleep(random.uniform(1, 5))
                                                    continue
                                        # except:
                                        #     print("damn")
                                        #     continue
                                        # finally:
                                                if success:
                                                    break

                            elif "www.dickssportinggoods.com" in s.lower():
                                await channel.send(scode + " it dicks")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        # try:
                                        print(
                                            f"using the proxy: {proxy.strip()}")
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(s) as response:
                                                print(response)
                                                print(response.status)
                                                if response.status == 200:
                                                    success = True
                                                    soup = BeautifulSoup(
                                                        await response.content, 'html.parser')
                                                    dicks_current_price = soup(
                                                        "span", {"class": "product-price ng-star-inserted"}).get_text()
                                                    insert_query = (
                                                        f"UPDATE shoes SET price = '{dicks_current_price}' WHERE url = '{s}';")
                                                    cursor.execute(
                                                        insert_query)
                                                    branddb.commit()
                                                    await channel.send(dicks_current_price)
                                                    await channel.send(s)
                                                else:
                                                    print(response.status)
                                                    print("damn")
                                                    await asyncio.sleep(random.uniform(1, 5))
                                                    continue
                                                await channel.send(s)
                                        # except:
                                        #     print("damn")
                                        #     continue
                                        # finally:
                                if success:
                                    break

                            elif "www.nordstrom.com" in s.lower():
                                await channel.send(scode + " it nordstrom")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        # try:
                                        print(
                                            f"using the proxy: {proxy.strip()}")
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(s) as response:
                                                print(response)
                                                print(response.status)
                                                if response.status == 200:
                                                    success = True
                                                    soup = BeautifulSoup(
                                                        await response.content, 'html.parser')
                                                    nord_current_price = soup.select_tone(
                                                        'div.ggbBg y3xFi span[aria-hidden="true"]')
                                                    if nord_current_price is not None:
                                                        nord_current_price = nord_current_price.get_text()
                                                    insert_query = (
                                                        f"UPDATE shoes SET price = '{nord_current_price}' WHERE url = '{s}';")
                                                    cursor.execute(
                                                        insert_query)
                                                    branddb.commit()
                                                    await channel.send(nord_current_price)
                                                    await channel.send(s)
                                                else:
                                                    print("damn")
                                                    continue
                                if success == True:
                                    break

                                    #     print("damn")
                                    #     continue
                                    # finally:
                                    #     if success:
                                    #         break

                            elif "www.mrporter.com" in s.lower():
                                await channel.send(scode + " it mrporter")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        try:
                                            print(
                                                f"using the proxy: {proxy.strip()}")
                                            res = requests.get(s, proxies={
                                                "http:": proxy.strip(),
                                                "https:": proxy.strip()
                                            }, headers=headers_rotate, timeout=5)
                                            print(res.status.code)
                                            if res.status_code == 200:
                                                success = True
                                                soup = BeautifulSoup(
                                                    res.content, 'html.parser')
                                                mrp_current_price = soup.find(
                                                    "span", {"itemprop": "price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{mrp_current_price}' WHERE url = '{s}';")
                                                cursor.execute(insert_query)
                                                branddb.commit()
                                                await channel.send(mrp_current_price)
                                            await channel.send(s)
                                        except:
                                            print("damn")
                                            continue
                                        finally:
                                            if success:
                                                break

                            elif "www.finishline.com" in s.lower():
                                await channel.send(scode + " it finishline")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        try:
                                            print(
                                                f"using the proxy: {proxy.strip()}")
                                            res = requests.get(s, proxies={
                                                "http:": proxy.strip(),
                                                "https:": proxy.strip()
                                            }, headers=headers_rotate, timeout=5)
                                            print(res.status.code)
                                            if res.status_code == 200:
                                                success = True
                                                soup = BeautifulSoup(
                                                    res.content, 'html.parser')
                                                finish_current_price = soup.find(
                                                    "div", {"class": "productPrice"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{finish_current_price}' WHERE url = '{s}';")
                                                cursor.execute(insert_query)
                                                branddb.commit()
                                                await channel.send(finish_current_price)
                                            await channel.send(s)
                                        except:
                                            print("damn")
                                            continue
                                        finally:
                                            if success:
                                                break

                            elif "www.footpatrol.com" in s.lower():
                                await channel.send(scode + " it footpatrol")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        try:
                                            print(
                                                f"using the proxy: {proxy.strip()}")
                                            res = requests.get(s, proxies={
                                                "http:": proxy.strip(),
                                                "https:": proxy.strip()
                                            }, headers=headers_rotate, timeout=5)
                                            print(res.status.code)
                                            if res.status_code == 200:
                                                success = True
                                                soup = BeautifulSoup(
                                                    res.content, 'html.parser')
                                                footpatrol_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{footpatrol_current_price}' WHERE url = '{s}';")
                                                cursor.execute(insert_query)
                                                branddb.commit()
                                                await channel.send(footpatrol_current_price)
                                            await channel.send(s)
                                        except:
                                            print("damn")
                                            continue
                                        finally:
                                            if success:
                                                break

                            elif "thehipstore.co.uk" in s.lower():
                                await channel.send(scode + " it hipstore")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        try:
                                            print(
                                                f"using the proxy: {proxy.strip()}")
                                            res = requests.get(s, proxies={
                                                "http:": proxy.strip(),
                                                "https:": proxy.strip()
                                            }, headers=headers_rotate, timeout=5)
                                            print(res.status.code)
                                            if res.status_code == 200:
                                                success = True
                                                soup = BeautifulSoup(
                                                    res.content, 'html.parser')

                                                hips_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{hips_current_price}' WHERE url = '{s}';")
                                                cursor.execute(insert_query)
                                                branddb.commit()
                                                await channel.send(hips_current_price)
                                            await channel.send(s)
                                        except:
                                            print("damn")
                                            continue
                                        finally:
                                            if success:
                                                break

                            elif "size.co.uk" in s.lower():
                                await channel.send(scode + " it size.co")
                                with open("valid_proxies.txt", "r") as vp:
                                    await channel.send("spinning")
                                    for proxy in vp:
                                        try:
                                            print(
                                                f"using the proxy: {proxy.strip()}")
                                            res = requests.get(s, proxies={
                                                "http:": proxy.strip(),
                                                "https:": proxy.strip()
                                            }, headers=headers_rotate, timeout=5)
                                            print(res.status.code)
                                            if res.status_code == 200:
                                                success = True
                                                soup = BeautifulSoup(
                                                    res.content, 'html.parser')
                                                size_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{size_current_price}' WHERE url = '{s}';")
                                                cursor.execute(insert_query)
                                                branddb.commit()
                                                await channel.send(size_current_price)
                                            await channel.send(s)
                                        except:
                                            print("damn")
                                            continue
                                        finally:
                                            if success:
                                                break
                            else:
                                await channel.send(f"{s} \n Na son, cloudfare\n")
                        except:
                            continue
                    await channel.send(sc_url_list_length)

    find_by_style_code = "find style"
    if lowermsg.startswith(find_by_style_code):
        await find_style_code()

    # adding shoes to db
    async def add_shoe():
        url = message.content
        if message.channel.id == 1074058028137070602:
            for b in br_table_array:
                url_input_list = url.split(", ")
                for new_url in url_input_list:
                    print(url_input_list)
                    if b.lower() in new_url.lower():
                        is_it = ("SELECT url FROM shoes")
                        cursor.execute(is_it)
                        is_it_table = cursor.fetchall()
                        is_it_table_array = [a for b in is_it_table for a in b]
                        if new_url in is_it_table_array:
                            await channel.send(new_url)
                            await channel.send("^^^dupe^^^")
                            if len(new_url.strip().split(",")) <= 1:
                                continue
                            return

                        group_a = (
                            "SELECT site_url FROM shoe_sites WHERE site_group = 'A'")
                        cursor.execute(group_a)
                        group_a_list = [a for b in cursor.fetchall()
                                        for a in b]
                        await channel.send(new_url)
                        for a in group_a_list:
                            await channel.send(a)
                            if a in new_url:
                                if new_url.endswith("/"):
                                    url = new_url[:-1]
                                else:
                                    url = new_url
                                sc = url.split('/').pop(-1)
                                name = url.split('/').pop(-2)
                                nmtrash = name.split('-').pop(-1)
                                if nmtrash in name:
                                    cleaned_name = name.replace(nmtrash, '')
                                    newname = cleaned_name.replace('-', ' ')
                                if "?" in sc:
                                    style_code = sc.split('?').pop(0)
                                    if "." in style_code:
                                        style_code = style_code.split(
                                            '.').pop(0)
                                elif "." in sc:
                                    style_code = sc.split('.').pop(0)
                                else:
                                    style_code = sc
                                insert_query = (
                                    "INSERT INTO shoes (name, style_code, url) VALUES (%s,%s,%s);"
                                )  # change brand to model
                                cursor.execute(
                                    insert_query, (newname, style_code, new_url))
                                branddb.commit()
                                await channel.send(f'Got it {newname} {style_code}')

                        group_b = (
                            "SELECT site_url FROM shoe_sites WHERE site_group = 'B'")
                        cursor.execute(group_b)
                        group_b_list = [a for b in cursor.fetchall()
                                        for a in b]

                        for sb in group_b_list:
                            await channel.send(sb)
                            if sb in new_url:
                                url = new_url
                                name_sty = url.split("/").pop(-1)
                                if "?" in name_sty:
                                    name_style = name_sty.split('?').pop(0)
                                else:
                                    name_style = name_sty
                                count = name_style.count("-") - 1
                                style_code = name_style.split(
                                    "-", count).pop(-1)
                                nmtrash = style_code
                                if nmtrash in name_style:
                                    cleaned_name = name_style.replace(
                                        nmtrash, '')
                                    newname = cleaned_name.replace('-', ' ')
                                insert_query = (
                                    "INSERT INTO shoes (name, style_code, url) VALUES (%s,%s,%s);"
                                )  # change brand to model
                                cursor.execute(
                                    insert_query, (newname, style_code, name_sty))
                                branddb.commit()
                                await channel.send(f'Got it {newname} {style_code}')
                                await channel.send(name_sty)
                                await channel.send(name_style)
                                await channel.send(count)
                                await channel.send(nmtrash)
                                await channel.send(newname)
                                await channel.send(style_code)

                        group_c = (
                            "SELECT site_url FROM shoe_sites WHERE site_group = 'C'")
                        cursor.execute(group_c)
                        group_c_list = [a for b in cursor.fetchall()
                                        for a in b]

                        for c in group_c_list:
                            if c in new_url:
                                await channel.send("Snipes is a nogo")

                        group_d = (
                            "SELECT site_url FROM shoe_sites WHERE site_group = 'D'")
                        cursor.execute(group_d)
                        group_d_list = [a for b in cursor.fetchall()
                                        for a in b]

                        for d in group_d_list:
                            if d in new_url:
                                url = new_url
                                if "?" in url:
                                    name_sty = url.split("?").pop(0)
                                else:
                                    name_sty = url
                                name_sty_trim = name_sty.split("/").pop(-1)
                                count = name_sty_trim.count("-")
                                style_code = name_sty_trim.split(
                                    "-", count).pop(-1)
                                nmtrash = style_code
                                if nmtrash in name_sty_trim:
                                    cleaned_name = name_sty_trim.replace(
                                        nmtrash, '')
                                    newname = cleaned_name.replace('-', ' ')
                                insert_query = (
                                    "INSERT INTO shoes (name, style_code, url) VALUES (%s,%s,%s);"
                                )  # change brand to model
                                cursor.execute(
                                    insert_query, (newname, style_code, name_sty))
                                branddb.commit()
                                await channel.send(f'Got it {newname} {style_code}')
                                await channel.send(name_sty)
                                await channel.send(name_sty_trim)
                                await channel.send(count)
                                await channel.send(nmtrash)
                                await channel.send(newname)
                                await channel.send(style_code)

                                # continue
        # threads = [threading.Thread(target=add_shoe) for _ in range(len(url_input_list))]
        # for t in threads:
        #     t.start()

                    # threads = []
                    # for input_data in url_input_list:
                    #     thread = threading.Thread(target=add_shoe, args=(input_data,))
                    #     thread.start()
                    #     threads.append(thread)

                    # for thread in threads:
                    #     thread.join()
        cursor.close()
    if any(message.content.startswith(p) for p in prefixes):
        await add_shoe()

    # search for shoe
    async def search_shoes():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=no+its+mine&limit=10") as response:
                print(response.status)
                if response.status == 200:
                    gifs_data = await response.json()
                    gifs = gifs_data["data"]
                    if gifs:
                        gif = random.choice(gifs)["url"]
                    await channel.send(gif)
            to_find = lowermsg[6:]
            found_shoes = (
                f"SELECT * FROM shoes WHERE name LIKE '%{to_find}%' OR url LIKE '%{to_find}%'")
            cursor.execute(found_shoes)
            all_found = cursor.fetchall()
            all_found_list = [a for b in all_found for a in b]
            clean = '\n'.join(map(str, all_found_list))
            # clean_list = [a for b in clean for a in b]
            await channel.send(clean)

    search = "gimme"
    if lowermsg.startswith(search):
        await search_shoes()

    if "commands" in lowermsg:
        await channel.send('''...
******************>
COMMANDS..........>
..................>
site list.........>
shoe list.........>
find style........>
add...............>
gimme.............>
freshen up beep>..>
help..............>
..................>
******************>''')

    if "help" in message.content.lower():
        await channel.send('''...

Send link to add shoe! As long as
 the site is in site list you str8!
Check the site list by sending
 "site list". No site in list?
Send "add" then the site followed
 by the appropriate format letter.
a, b, c, or d. "www.store.com a"

**Don't worry about
the rest(?=>) part of the url**

Format A
.com/blah/n-a-m-e/scORsku

Format B
.com/blah/n-a-m-e-sc-sc

Format C
dont work

Format D
.com/blah/n-a-m-e-sc

Multi-link input only registers the
sites coming from the first in the
list. Seperate them with a , .

https://www.n.com/no/win,
www.f.com/af/shoe-09, www.g.com/e,
http://www.flb.com/clo

Check all shoes list in the db by
 sending "shoe list"

Check for current prices in db by
 sending "find style" followed by
 the style code.One code at a time

find style CHJKS-9878

Refresh the proxies by sending
"freshen up beep"

Search for shoes in database by
sending "gimme" followed by search
words''')


###BEEPAI###


    async def message_to_dict(message):
        return {
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    # async def generate_response(message):
    #     message_dict = await message_to_dict(message)
    #     params = {'prompt': message_dict['content']}
    #     response = openai.Completion.create(
    #         engine="text-davinci-003",
    #         prompt=message.content,
    #         max_tokens=10,
    #         n=1,
    #         stop=None,
    #         temperature=0.1,
    #     )
    #     generated_text = response["choices"][0]["text"]

    #     # Send generated text back to Discord
    #     await message.channel.send(generated_text)
    #     await channel.send("gr^^^")
    no_no = ["site list", "shoe list", "find style",
             "add", "gimme", "freshen up beep", "help"]
    punct = [".", "?", "!"
             ]
    punct_message = message.content.endswith(('.', '?', '!'))
    discord_user_id = message.author.id
    username = message.author.name
    print(punct_message)

    async def handle_message():

        async with aiomysql.create_pool(
            host='Localhost',
            port=3306,
            user='root',
            password='root',
            db='beep_ai'
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    select_user_query = "SELECT user_id FROM users WHERE discord_user_id=%s"
                    await cursor.execute(select_user_query, (discord_user_id))
                    result = await cursor.fetchone()

                    if result is None:
                        insert_user_query = "INSERT INTO users (discord_user_id, username) VALUES (%s, %s)"
                        await cursor.execute(insert_user_query, (discord_user_id, username))
                        await conn.cssswommit()
                        print("added new user")
                    else:
                        print("known user")

                    user_id = result[0]
                    # message_dict = await message_to_dict(message)
                    # params = {'prompt': message_dict['content']}
                    # message_content = message.content + "."
                    # select_query = "SELECT bot_response FROM interactions WHERE user_id=%s ORDER BY interaction_timestamp DESC LIMIT 10"
                    # await cursor.execute(select_query, (user_id))
                    # previous_resp = await cursor.fetchall()
                    # prev_resp_list = [resp[0] for resp in previous_resp]
                    # prev_resp_str = " ".join(prev_resp_list)
                    # prompt = prev_resp_str + " " + message.content
                    if punct_message == True:
                        response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=message.content,
                            max_tokens=100,
                            n=1,
                            top_p=1,
                            stop=None,
                            frequency_penalty=0,
                            presence_penalty=0,
                            temperature=0
                        )
                        generated_text = response["choices"][0]["text"]

                        # Send generated text back to Discord
                        print(generated_text)
                        await message.channel.send(generated_text)
                        await channel.send("gr^^^")
                        insert_interaction_query = "INSERT INTO interactions (user_id, context, bot_response) VALUES (%s, %s, %s)"
                        await cursor.execute(insert_interaction_query, (user_id, message.content, generated_text))
                        await conn.commit()

        # result = await handle_message(discord_user_id, username, message)
        # await channel.send(result)
        # await channel.send("res^^^")
    await handle_message()

bot.run(TOKEN)
