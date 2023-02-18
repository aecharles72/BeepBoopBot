# async functions


def startup_proxies(requests, time, random, now_time, modified_file_time, current_new_proxies, ip_token):
    if now_time - modified_file_time > 1800:
        with open("proxy_list.txt", "w") as pl:
            print(now_time)
            print(modified_file_time)
            fresh_proxie = current_new_proxies[75:]
            pl.write(fresh_proxie)
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
                    print(res.status_code)
                    if res.status_code == 200:
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

# add site to site list


async def add_site(br_table_array, message, channel, cursor, branddb, br_list):
    breakdown = message.content.split()
    for site in breakdown:
        if breakdown[1] in br_table_array:
            await channel.send('already there man')
            return
        else:
            insert_site = (
                f"INSERT INTO shoe_sites (site_url, site_group) VALUE ('{breakdown[1]}','{breakdown[2].upper()}');")
            await cursor.execute(insert_site)
            await branddb.commit()
            await channel.send("added")
            await channel.send(f"...\nAdded {breakdown[1].upper()} to group {breakdown[2].upper()} in list:\n{br_list}")
            return


async def del_site(br_table_array, message, channel, cursor, branddb):
    site_to_del = message.content[7:].lower()
    print(site_to_del)
    find_site = f"SELECT id FROM shoe_sites WHERE site_url = '{site_to_del}'"
    print(find_site)
    await cursor.execute(find_site)
    found = await cursor.fetchone()
    print(found)
    found_id = found[0]
    print(found_id)
    delete_site = f"DELETE FROM shoe_sites WHERE id = '{found_id}'"
    print(delete_site)
    await cursor.execute(delete_site)
    await branddb.commit()
    await channel.send(f"{found} gone")


async def fresh_while_on(aiofiles, current_new_proxies):
    async with aiofiles.open("proxy_list.txt", "w") as pl:
        fresh_proxies = current_new_proxies[75:]
        await pl.write(fresh_proxies)
        print("Done adding fresh proxies")
        await pl.close()


async def check_while_on(aiofiles, aiohttp, asyncio, random, ip_token, channel):
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


async def get_soup(aiohttp, BeautifulSoup, s, channel):
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
                        return soup, success


async def add_group_a(a, new_url, cursor, branddb, channel):
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
    await cursor.execute(
        insert_query, (newname, style_code, new_url))
    await branddb.commit()
    await channel.send(f'Got it {newname} {style_code}')


async def add_group_b(sb, new_url, cursor, branddb, channel):
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
    await cursor.execute(
        insert_query, (newname, style_code, name_sty))
    await branddb.commit()
    await channel.send(f'Got it {newname} {style_code}')
    # await channel.send(name_sty)
    # await channel.send(name_style)
    # await channel.send(count)
    # await channel.send(nmtrash)
    # await channel.send(newname)
    # await channel.send(style_code)


async def add_group_d(new_url, cursor, branddb, channel):
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
    await cursor.execute(
        insert_query, (newname, style_code, name_sty))
    await branddb.commit()
    await channel.send(f'Got it {newname} {style_code}')
    # await channel.send(name_sty)
    # await channel.send(name_sty_trim)
    # await channel.send(count)
    # await channel.send(nmtrash)
    # await channel.send(newname)
    # await channel.send(style_code)

# adding shoes to db


async def add_shoe(message, channel, cursor, branddb, br_table_array):
    url = message.content
    url_input_list = [u.strip() for u in url.split(",")]
    # print(url_input_list)
    # print(br_table_array)
    match_list = [
        match for match in url_input_list for b in br_table_array if b.lower() in match.lower()]
    # print(match_list)
    for new_url in match_list:
        is_it = ("SELECT url FROM shoes")
        await cursor.execute(is_it)
        is_it_table = await cursor.fetchall()
        is_it_table_array = [a for b in is_it_table for a in b]
        if new_url in is_it_table_array:
            await channel.send("^^^dupe^^^")
            if len(new_url.strip().split(",")) >= 1:
                continue
            return

        group_a = (
            "SELECT site_url FROM shoe_sites WHERE site_group = 'A'")
        await cursor.execute(group_a)
        group_a_list = [a for b in await cursor.fetchall()
                        for a in b]
        for a in group_a_list:
            if a in new_url:
                await add_group_a(a, new_url, cursor, branddb, channel)
                break

        group_b = (
            "SELECT site_url FROM shoe_sites WHERE site_group = 'B'")
        await cursor.execute(group_b)
        group_b_list = [a for b in await cursor.fetchall()
                        for a in b]
        for sb in group_b_list:
            if sb in new_url:
                await add_group_b(sb, new_url, cursor, branddb, channel)
                break

        group_c = (
            "SELECT site_url FROM shoe_sites WHERE site_group = 'C'")
        await cursor.execute(group_c)
        group_c_list = [a for b in await cursor.fetchall()
                        for a in b]
        for c in group_c_list:
            if c in new_url:
                await channel.send("Snipes is a nogo")
                break

        group_d = (
            "SELECT site_url FROM shoe_sites WHERE site_group = 'D'")
        await cursor.execute(group_d)
        group_d_list = [a for b in await cursor.fetchall()
                        for a in b]
        for d in group_d_list:
            if d in new_url:
                await add_group_d(new_url, cursor, branddb, channel)
                break

# search for shoe


async def search_shoes(aiohttp, random, GIPHY_TOKEN, lowermsg, cursor, branddb, channel):
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
        await cursor.execute(found_shoes)
        all_found = await cursor.fetchall()
        all_found_list = [a for b in all_found for a in b]
        clean = '\n'.join(map(str, all_found_list))
        # clean_list = [a for b in clean for a in b]
        await channel.send(clean)


def check(message, author, channel):
    return author == message.author and channel == message.channel


async def new_thread(discord, bot, message, channel, thread_name, thread_reason):
    text_channel = discord.utils.get(message.guild.channels, name='threads')
    if not text_channel:
        text_channel = await channel.category.create_text_channel('threads')
    thread = await text_channel.create_thread(
        name=thread_name,
        auto_archive_duration=0,
        reason=thread_reason)
    fresh_thread = discord.utils.get(
        message.guild.threads, name=thread_name)
    await text_channel.send(
        f'"{message.author}" created in {text_channel.mention}!\n{thread.mention}', mention_author=True)
    await fresh_thread.send(f'{message.author.mention} your private thread')


async def make_new_thread(discord, bot, asyncio, message, check, channel, author):
    await channel.send("Gimme name 30 SECONDS!")
    next_resp = False
    def check_(m): return check(m, author, channel)
    try:
        # Wait for the user's response
        response = await bot.wait_for('message', check=check_, timeout=30)
        thread_name = response.content
        next_resp = True
    except asyncio.TimeoutError:
        await channel.send("Too slow, try again!")
    if next_resp == True:
        await channel.send("Ok but why? 30 SECONDS!")
        try:
            response = await bot.wait_for('message', check=check_, timeout=30)
            thread_reason = response.content
        except asyncio.TimeoutError:
            await channel.send("Too slow, try again!")
        finally:
            await new_thread(discord, bot, message, channel, thread_name, thread_reason)
