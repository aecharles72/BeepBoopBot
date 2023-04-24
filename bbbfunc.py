"""
Beep functions

"""
import asyncio
import hashlib


def cancel_task(task):
    '''


    Parameters
    ----------
    task : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    if not task.done():
        task.cancel()


def check(message, author, channel):
    '''
    Parameters
    ----------
    message : TYPE v
    author : TYPE v
    channel : TYPE v
        DESCRIPTION.
        check

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''

    return author == message.author and channel == message.channel


async def new_site_user(aiomysql, bot, message, member, channel):

    author = message.author
    try:
        async with aiomysql.create_pool(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='beep_site'
        ) as beep_site:
            print("PASS: 1")
            async with beep_site.acquire() as site_users:
                async with site_users.cursor() as site_users_cursor:
                    next_resp = False
                    print("PASS: 2")

                    def check_(m):
                        return check(m, author, channel)
                    print("PASS: 3")
                    try:
                        await channel.send("Username must be 3-10 characters\n\
                                           E-mail must be a valid US e-mail address\n\
                                               You have 30 seconds\n\
                                               Username & Email:")
                        print("PASS: 4")
                        # Wait for the user's response
                        response = await bot.wait_for('message', check=check_, timeout=30)
                        print(f"PASS: {response}")
                        thread_author = response.author
                        split_mess = response.content.split()
                        author_nick = split_mess[0]
                        print(f"PASS: {author_nick}")
                        author_email = split_mess[1]
                        print(f"PASS: {author_email}")
                        must_end = (".com", ".org", ".edu", ".co")
                        cant_be = ("admin", "eddiebueno")
                        if author_nick.lower() in cant_be:
                            await channel.send("Try again")
                            return
                        if any(message.content.endswith(must_end) for end in must_end):
                            if "@" not in author_email or not author_email.endswith(must_end) or len(author_nick) < 3 or len(split_mess) != 2:
                                await channel.send("Invalid.\n\
                            Must have a space between username and valid email address.")
                                return
                        print(f"PASS: {thread_author}")
                        print(f"PASS: {author_email}")

                        is_it = f"SELECT email FROM users \
                            WHERE email = '{author_email}'"
                        print(f"PASS: {is_it}")
                        await site_users_cursor.execute(is_it)
                        it_is = await site_users_cursor.fetchone()
                        print(f"PASS: {it_is}")
                        if it_is is not None:
                            taken = await channel.send(
                                "https://giphy.com/gifs/taken-seat-kDRacElvbMPDO\nThis e-mail is \
                                    already associated to a user")
                            await taken.delete(delay=10)
                            return
                        next_resp = True
                    except asyncio.TimeoutError:
                        await channel.send("Too slow, try again!")
                    if next_resp is True:
                        await channel.send("Password must be 3-10 characters\n\n\
                                           PLEASE BE AWARE WHEN YOU HIT ENTER\n\
                                           YOUR PASSWORD WILL BE SET AND THE\n\
                                           MESSAGE WILL BE DELETED\n\n\
                                               You have 40 seconds\n\
                                           What's your password?")
                        try:
                            response = await bot.wait_for('message', check=check_, timeout=40)
                            author_password = response.content
                            if len(author_password) < 3 or len(author_password) > 10:
                                await channel.send("Invalid Password")
                                return
                        except asyncio.TimeoutError:
                            await channel.send("Too slow, try again!")
                        finally:
                            salt = 'XyZzy12*_'
                            hashed_password = hashlib.md5(
                                (salt + author_password).encode('utf-8')
                            ).hexdigest()
                            new_site_user = f"INSERT INTO users (name, email, password, discord_user_id) VALUES \
                                ('{author_nick}','{author_email}','{hashed_password}', '{member.id}')"
                            await site_users_cursor.execute(new_site_user)
                            await site_users.commit()
                            get_new_user_id = f"SELECT user_id FROM users WHERE name = '{author_nick}'"
                            await site_users_cursor.execute(get_new_user_id)
                            new_users_id = await site_users_cursor.fetchone()
                            new_users_id = new_users_id[0]
                            new_users_profile = f"INSERT INTO profile (user_id, name, email) VALUES\
                                ('{new_users_id}', '{author_nick}','{author_email}')"
                            await site_users_cursor.execute(new_users_profile)
                            await site_users.commit()
                            await response.delete()
                            await channel.send(
                                "Account created! Head over to www.eddiebueno.com/beepboop")
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def tup_to_list(argx):
    '''


    Parameters
    ----------
    argx : TYPE
        DESCRIPTION.

    Returns
    -------
    arg_list : TYPE
        DESCRIPTION.

    '''
    tup = argx
    arg_list = [a for b in tup for a in b]
    return arg_list


async def tup_to_str(argx):
    '''


    Parameters
    ----------
    argx : TYPE
        DESCRIPTION.

    Returns
    -------
    arg_str : TYPE
        DESCRIPTION.

    '''
    tup = argx
    arg_list = [a for b in tup for a in b]
    arg_str = ''.join(arg_list)
    return arg_str


async def tup_to_str_list(argx):
    '''


    Parameters
    ----------
    argx : TYPE
        DESCRIPTION.

    Returns
    -------
    arg_str : TYPE
        DESCRIPTION.

    '''
    tup = argx
    arg_list = [a for b in tup for a in b]
    arg_str = '\n'.join(arg_list)
    return arg_str


async def tup_to_dict(argx):
    '''


    Parameters
    ----------
    argx : TYPE
        DESCRIPTION.

    Returns
    -------
    arg_dict : TYPE
        DESCRIPTION.

    '''
    tup = argx
    arg_list = [a for b in tup for a in b]
    arg_dict = dict(zip(arg_list[::2], arg_list[1::2]))
    return arg_dict


async def tuptup_to_dict(argx):
    '''


    Parameters
    ----------
    argx : TYPE
        DESCRIPTION.

    Returns
    -------
    arg_dict : TYPE
        DESCRIPTION.

    '''
    arg_dict = []

    for tup in argx:
        tup_dict = {'tup_key': tup[0], 'tup_val': tup[1]}
        arg_dict.append(tup_dict)
    return arg_dict


async def is_pin(message):
    '''


    Parameters
    ----------
    message : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    print(f"ISPIN: {message}")
    if message.pinned is True:
        print("ISPIN: TRUE")
        return False
    else:
        print("ISPIN: FALSE")
        return True


def startup_proxies(
        requests, time, random, now_time, modified_file_time, current_new_proxies, ip_token):
    '''


    Parameters
    ----------
    requests : TYPE lib
    time : TYPE lib
    random : TYPE lib
    now_time : TYPE v
    modified_file_time : TYPE v
    current_new_proxies : TYPE v
    ip_token : TYPE env
        DESCRIPTION.
        startup proxy list setup

    Returns
    ----
    None.

    '''
    if now_time - modified_file_time > 43200:
        with open("proxy_list.txt", "w", encoding="utf-8") as p_l:
            print(f"START: {now_time}")
            print(f"START: {modified_file_time}")
            fresh_proxie = current_new_proxies[75:]
            p_l.write(fresh_proxie)
            print("START: Done adding fresh proxies")
            p_l.close()
        with open("proxy_list.txt", "r", encoding="utf-8") as o_l:
            proxies = o_l.read().split("\n")
            valid_proxies = []
            for proxy in proxies:
                check_p = proxy.split(":").pop(0)
                checker = f"https://ipinfo.io/{check_p}/json?token={ip_token}"
                print(f"START: {proxy}")
                with requests.get(checker) as res:
                    print(f"START: {res.status_code}")
                    if res.status_code == 200:
                        valid_proxies.append(proxy)
                    else:
                        time.sleep(random.uniform(1, 5))
                    if res.status_code == 429:
                        break
                o_l.close()

        with open("valid_proxies.txt", "w", encoding="utf-8") as v_p:
            v_p.write("\n".join(valid_proxies))
            print(f"START: {now_time}""done check")
            v_p.close()


async def add_site(br_table_array, message, channel, cursor, branddb, br_list):
    '''


    Parameters
    ----------
    br_table_array : TYPE info
    message : TYPE v
    channel : TYPE v
    cursor : TYPE v
    branddb : TYPE aiodb
    br_list : TYPE info
        DESCRIPTION.
        add site to site list

    Returns
    -------
    None.

    '''
    breakdown = message.content.split()
    if breakdown[1] in br_table_array:
        await channel.send('already there man')
        return
    insert_site = (
        f"INSERT INTO shoe_sites (site_url, site_group) VALUE \
            ('{breakdown[1]}','{breakdown[2].upper()}');")
    await cursor.execute(insert_site)
    await branddb.commit()
    await channel.send("added")
    await channel.send(
        f"...\nAdded {breakdown[1].upper()} to group {breakdown[2].upper()} in list:\n{br_list}")


async def del_site(message, channel, cursor, branddb):
    '''


    Parameters
    ----------
    message : TYPE v
    channel : TYPE v
    cursor : TYPE v
    branddb : TYPE aiodb
        DESCRIPTION.
        delete site from site list

    Returns
    -------
    None.

    '''
    try:
        site_to_del = message.content[7:].lower()
        print(f"DELSITE: {site_to_del}")
        find_site = f"SELECT id FROM shoe_sites WHERE site_url = '{site_to_del}'"
        print(f"DELSITE: {find_site}")
        await cursor.execute(find_site)
        found = await cursor.fetchone()
        print(f"DELSITE: {found}")
        found_id = found[0]
        print(f"DELSITE: {found_id}")
        delete_site = f"DELETE FROM shoe_sites WHERE id = '{found_id}'"
        print(f"DELSITE: {delete_site}")
        await cursor.execute(delete_site)
        await branddb.commit()
        await channel.send(f"{found} gone")
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def fresh_while_on(aiofiles, current_new_proxies):
    '''


    Parameters
    ----------
    aiofiles : TYPE lib
    current_new_proxies : TYPE v
        DESCRIPTION.
        refresh proxy list while running

    Returns
    -------
    None.

    '''
    async with aiofiles.open("proxy_list.txt", "w") as p_l:
        fresh_proxies = current_new_proxies[75:]
        await p_l.write(fresh_proxies)
        print("FRESHWO: Done adding fresh proxies")
        await p_l.close()


async def check_while_on(aiofiles, aiohttp, ip_token, channel, now_time, modified_file_time):
    '''


    Parameters
    ----------
    aiofiles : TYPE lib
    aiohttp : TYPE lib
    asyncio : TYPE lib
    ip_token : TYPE env
    channel : TYPE v
        DESCRIPTION.
        validate proxies while running

    Returns
    -------
    None.

    '''
    if now_time - modified_file_time > 21600:
        valid_proxies = []
        print("Begin Check")
        async with aiofiles.open("proxy_list.txt", "r") as p_l:
            proxies = ''.join(await p_l.read()).split()
            valid_proxies = []
            async with aiohttp.ClientSession() as session:

                for proxy in proxies:
                    check_p = proxy.split(":").pop(0)
                    checker = f"https://ipinfo.io/{check_p}/json?token={ip_token}"
                    print(f"CHECKWO: {proxy}")
                    async with session.get(checker) as res:
                        print(f"CHECKWO: {res.status}")
                        if res.status == 200:
                            valid_proxies.append(proxy)
                            await asyncio.sleep(.25)
                        else:
                            await asyncio.sleep(.5)
                        if res.status == 429:
                            await channel.send("429 DEAD")
                            await asyncio.sleep(1)
                            break
            async with aiofiles.open("valid_proxies.txt", "w") as o_l:
                await o_l.write("\n".join(valid_proxies))


async def get_soup(aiohttp, BeautifulSoup, s, channel):
    """
    # unused

    """
    with open("valid_proxies.txt", "r", encoding="utf-8") as v_p:
        await channel.send("spinning")
        for proxy in v_p:
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


async def add_group_a(new_url, cursor, branddb, channel, author_id):
    '''


    Parameters

    new_url : TYPE v
    cursor : TYPE v 
    branddb : TYPE aiodb
    channel : TYPE v
    author_id : TYPE v
        DESCRIPTION.
        parse an A link

    Returns
    -------
    None.

    '''
    try:
        if new_url.endswith("/"):
            url = new_url[:-1]
        else:
            url = new_url
        s_c = url.split('/').pop(-1)
        name = url.split('/').pop(-2)
        nmtrash = name.split('-').pop(-1)
        if nmtrash in name:
            cleaned_name = name.replace(nmtrash, '')
            newname = cleaned_name.replace('-', ' ')
        if "?" in s_c:
            style_code = s_c.split('?').pop(0)
            if "." in style_code:
                style_code = style_code.split(
                    '.').pop(0)
        elif "." in s_c:
            style_code = s_c.split('.').pop(0)
        else:
            style_code = s_c
        insert_query = (
            "INSERT INTO shoes (name, style_code, url, discord_user_id) VALUES (%s,%s,%s,%s);"
        )  # change brand to model
        await cursor.execute(
            insert_query, (newname, style_code, new_url, author_id))
        await branddb.commit()
        await channel.send(f'Got it {newname} {style_code}')
        # checks
        # await channel.send(url
        # await channel.send(sc)
        # await channel.send(name)
        # await channel.send(nmtrash)
        # await channel.send(newname)
        # await channel.send(style_code)
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def add_group_b(new_url, cursor, branddb, channel, author_id):
    '''


    Parameters
    ----------
    new_url : TYPE v
    cursor : TYPE v
    branddb : TYPE aiodb
    channel : TYPE v
    author_id : TYPE v
        DESCRIPTION.
        parse a B link

    Returns
    -------
    None.

    '''
    try:
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
            "INSERT INTO shoes (name, style_code, url, discord_user_id) VALUES (%s,%s,%s,%s);"
        )
        await cursor.execute(
            insert_query, (newname, style_code, name_sty, author_id))
        await branddb.commit()
        await channel.send(f'Got it {newname} {style_code}')
        # checks
        # await channel.send(name_sty)
        # await channel.send(name_style)
        # await channel.send(count)
        # await channel.send(nmtrash)
        # await channel.send(newname)
        # await channel.send(style_code)
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def add_group_d(new_url, cursor, branddb, channel, author_id):
    '''


    Parameters
    ----------
    new_url : TYPE v
    cursor : TYPE v
    branddb : TYPE aiodb
    channel : TYPE v
    author_id : TYPE v
        DESCRIPTION.
        parse a D link

    Returns
    -------
    None.

    '''
    try:
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
            "INSERT INTO shoes (name, style_code, url, discord_user_id) VALUES (%s,%s,%s,%s);"
        )
        await cursor.execute(
            insert_query, (newname, style_code, name_sty, author_id))
        await branddb.commit()
        await channel.send(f'Got it {newname} {style_code}')
        # checks
        # await channel.send(name_sty)
        # await channel.send(name_sty_trim)
        # await channel.send(count)
        # await channel.send(nmtrash)
        # await channel.send(newname)
        # await channel.send(style_code)
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def add_shoe(message, channel, cursor, branddb, br_table_array):
    '''


    Parameters
    ----------
    message : TYPE v
    channel : TYPE v
    cursor : TYPE v
    branddb : TYPE aiodb
    br_table_array : TYPE info
        DESCRIPTION.
        adding shoes to db

    Returns
    -------
    None.

    '''
    try:
        url = message.content
        url_input_list = [u.strip() for u in url.split(",")]
        # print(url_input_list)
        # print(br_table_array)
        author_id = message.author.id
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

            # group A check
            group_a = (
                "SELECT site_url FROM shoe_sites WHERE site_group = 'A'")
            await cursor.execute(group_a)
            group_a_list = [a for b in await cursor.fetchall()
                            for a in b]
            for site in group_a_list:
                if site in new_url:
                    await add_group_a(new_url, cursor, branddb, channel, author_id)
                    break

            # group B check
            group_b = (
                "SELECT site_url FROM shoe_sites WHERE site_group = 'B'")
            await cursor.execute(group_b)
            group_b_list = [a for b in await cursor.fetchall()
                            for a in b]
            for site in group_b_list:
                if site in new_url:
                    await add_group_b(new_url, cursor, branddb, channel, author_id)
                    break

            # group C check
            group_c = (
                "SELECT site_url FROM shoe_sites WHERE site_group = 'C'")
            await cursor.execute(group_c)
            group_c_list = [a for b in await cursor.fetchall()
                            for a in b]
            for site in group_c_list:
                if site in new_url:
                    await channel.send("Snipes is a nogo")
                    break

            # group D check
            group_d = (
                "SELECT site_url FROM shoe_sites WHERE site_group = 'D'")
            await cursor.execute(group_d)
            group_d_list = [a for b in await cursor.fetchall()
                            for a in b]
            for site in group_d_list:
                if site in new_url:
                    await add_group_d(new_url, cursor, branddb, channel, author_id)
                    break
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def search_shoes(discord, aiohttp, random, GIPHY_TOKEN, lowermsg, cursor, channel):
    '''


    Parameters
    ----------
    aiohttp : TYPE lib
    random : TYPE lib
    GIPHY_TOKEN : TYPE env
    lowermsg : TYPE v
    cursor : TYPE v
    channel : TYPE v
        DESCRIPTION.
        search in shoes table

    Returns
    -------
    None.

    '''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=loading&limit=10"
            ) as response:
                async with session.get(
                    f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q=no+its+mine&limit=10"
                ) as bad_response:
                    print(f"SEARCH: {response.status}")
                    if response.status == 200:
                        gifs_data = await response.json()
                        gifs = gifs_data["data"]
                        if gifs:
                            gif = random.choice(gifs)["url"]
                        send_gif = await channel.send(gif)
                        await send_gif.delete(delay=2)
                to_find = lowermsg[6:]
                found_shoes = (
                    f"SELECT * FROM shoes WHERE name LIKE '%{to_find}%' OR url LIKE '%{to_find}%'")
                await cursor.execute(found_shoes)
                all_found = await cursor.fetchall()
                if all_found:
                    page = 1
                    while len(all_found) > 0:
                        embed = discord.Embed(
                            title='Search Results', description=f'Search query: {to_find}',
                            color=discord.Color.blue())
                        for result in all_found[:20]:
                            name = result[1]
                            nick_name = result[2]
                            style_code = result[3]
                            color = result[4]
                            og_price = result[5]
                            cur_price = result[6]
                            url = result[7]
                            embed.add_field(
                                name=name, value=f'Nickname: {nick_name}\nStyle Code: {style_code}\nColor: \
{color}\nOld Price:{og_price}\nCurrent Price: {cur_price}\nURL: <{url}>', inline=False)
                        send_embed = await channel.send(embed=embed)
                        await send_embed.delete(delay=600)
                        all_found = all_found[20:]
                        page += 1

                        if len(all_found) > 0:
                            if bad_response.status == 200:
                                gifs_data = await response.json()
                                gifs = gifs_data["data"]
                                if gifs:
                                    gif = random.choice(gifs)["url"]
                                send_bad = await channel.send(gif)
                            await send_bad.delete(delay=10)
                            await channel.send(f"Page {page} of search results. \
Be more specific for refined results.")
                else:
                    await channel.send("No results found.")
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def shoe_list(discord, channel, cursor, branddb, member):
    '''


    Parameters
    ----------
    discord : TYPE
        DESCRIPTION.
    channel : TYPE
        DESCRIPTION.
    cursor : TYPE
        DESCRIPTION.
    branddb : TYPE
        DESCRIPTION.
    member : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    task_query = f"INSERT INTO tasks_ran (task_name, discord_user_id) VALUES ('task_shoe_list',\
        '{member.id}')"
    await cursor.execute(task_query)
    await asyncio.sleep(1)
    s_h = ("SELECT name FROM shoes")
    await cursor.execute(s_h)
    shoe_table = await cursor.fetchall()
    # print(shoe_table)
    shoes_list = await tup_to_list(shoe_table)
    # print(shoes_list)
    # embed = discord.Embed(title="Shoe List", description='\n'.join(shoes_list))
    max_items_per_embed = 100
    total_embeds = (len(shoes_list) // max_items_per_embed) + 1
    print(f"SHLIST: {total_embeds}")
    for i in range(total_embeds):
        embed = discord.Embed(title="Super Long Shoe List WHY DID YOU EVEN", description="")
        start_index = i * max_items_per_embed
        end_index = min(start_index + max_items_per_embed, len(shoes_list))
        for item in shoes_list[start_index:end_index]:
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
    await branddb.commit()
    return


async def new_thread(discord, message, channel, thread_name, thread_reason, thread_author):
    '''

    Parameters
    ----------
    discord : TYPE lib
    message : TYPE v
    channel : TYPE v
    thread_name : TYPE v
    thread_reason : TYPE v
    thread_author : TYPE v
        DESCRIPTION.
        # makes new thread using params

    Returns
    -------
    None.

    '''
    try:
        guild = message.guild
        text_channel = discord.utils.get(guild.channels, name='threads')
        if not text_channel:
            text_channel = await channel.category.create_text_channel('threads')
        thread = await text_channel.create_thread(
            name=thread_name,
            auto_archive_duration=0,
            invitable=False,
            reason=thread_reason)
        fresh_thread = discord.utils.get(
            guild.threads, name=thread_name)
        new_role = await guild.create_role(name=thread_name)
        await fresh_thread.add_user(thread_author)
        await thread_author.add_roles(new_role)
        await text_channel.send(
            f'"{message.author}" created in {text_channel.mention}!\n{thread.mention}',
            mention_author=True)
        pin_message = await fresh_thread.send('''***
    SITE LIST👀  SHOE LIST👟  FIND STYLE💵  CLEAR🧹
    ADD SITE👍🏾   DEL SITE👎🏾   REFRESH🌪️   SCOOP📥
    GIMME🔍   COMMANDS🤬   HELP❓   ADD SHOE📚 ''')
        await pin_message.add_reaction("👀")
        await pin_message.add_reaction("👟")
        await pin_message.add_reaction("💵")
        await pin_message.add_reaction("🔍")
        await pin_message.add_reaction("🔑")
        await pin_message.add_reaction("🤬")
        await pin_message.add_reaction("❓")
        await pin_message.add_reaction("📚")
        await pin_message.add_reaction("📥")
        await pin_message.add_reaction("👍🏾")
        await pin_message.add_reaction("👎🏾")
        await pin_message.add_reaction("🌪️")
        await pin_message.add_reaction("🧹")
        # await pin_message.add_reaction("❌")
        await pin_message.pin()
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def make_new_thread(aiomysql, discord, bot, message, check, channel, author):
    '''


    Parameters
    ----------
    aiomysql : TYPE lib
    discord : TYPE lib
    bot : TYPE client
    asyncio : TYPE lib
    message : TYPE v
    check : TYPE func
    channel : TYPE v
    author : TYPE v
        DESCRIPTION.
        NEW THREAD CREATION
    Returns
    -------
    None.

    '''
    try:
        async with aiomysql.create_pool(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='beep_ai'
        ) as beep_ch:
            print("THREAD: 1")
            async with beep_ch.acquire() as beep_chan:
                async with beep_chan.cursor() as beep_chan_cursor:
                    await channel.send("Gimme name 30 SECONDS!")
                    next_resp = False
                    print("THREAD: 2")

                    def check_(m):
                        return check(m, author, channel)
                    print("THREAD: 3")
                    try:
                        print("THREAD: 4")
                        # Wait for the user's response
                        response = await bot.wait_for('message', check=check_, timeout=30)
                        print(f"THREAD: {response}")
                        thread_author = response.author
                        thread_name = response.content
                        no_good = ["Admin", "Beep Boop", "User"]
                        if thread_name in no_good:
                            await channel.send("Nice try")
                            return
                        print(f"THREAD: {thread_author}")
                        print(f"THREAD: {thread_name}")
                        is_it = f"SELECT thread_name FROM beep_channels \
                            WHERE thread_name = '{thread_name}'"
                        print(f"THREAD: {is_it}")
                        await beep_chan_cursor.execute(is_it)
                        it_is = await beep_chan_cursor.fetchone()
                        print(f"THREAD: {it_is}")
                        if it_is is not None:
                            taken = await channel.send(
                                "https://giphy.com/gifs/taken-seat-kDRacElvbMPDO")
                            await taken.delete(delay=10)
                            return
                        next_resp = True
                    except asyncio.TimeoutError:
                        await channel.send("Too slow, try again!")
                    if next_resp is True:
                        await channel.send("Ok but why? 30 SECONDS!")
                        try:
                            response = await bot.wait_for('message', check=check_, timeout=30)
                            thread_reason = response.content
                        except asyncio.TimeoutError:
                            await channel.send("Too slow, try again!")
                        finally:
                            thread_reason = response.content
                            await new_thread(discord,
                                             message,
                                             channel,
                                             thread_name,
                                             thread_reason,
                                             thread_author)
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


async def beep_channels(discord, aiomysql, message):
    '''
    Parameters
    ----------
    aiomysql : TYPE lib
    message : TYPE v
        DESCRIPTION.
        get channel info of guild
        create a new thread

    Returns
    -------
    None.

    '''
    print("BEEPCH in channel")

    # beep ai db
    try:
        async with aiomysql.create_pool(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='beep_ai'
        ) as beep_ch:
            async with beep_ch.acquire() as beep_chan:
                async with beep_chan.cursor() as beep_chan_cursor:
                    channel_id = message.channel.id
                    # print(f"BEEPCH: {channel_id}")
                    channel_name = message.channel
                    print(f"BEEPCH: {channel_name}")
                    discord_user_id = message.author.id
                    # print(f"BEEPCH: {discord_user_id}")
                    check_channels = f"SELECT thread_id FROM beep_channels WHERE thread_id = \
                        '{channel_id}'"
                    await beep_chan_cursor.execute(check_channels)
                    result_1 = await beep_chan_cursor.fetchone()
                    check_channels = f"SELECT thread_name FROM beep_channels WHERE thread_name = \
                        '{channel_name}'"
                    await beep_chan_cursor.execute(check_channels)
                    result_2 = await beep_chan_cursor.fetchone()
                    if result_1 is None and result_2 is None:
                        insert_channels = f"INSERT INTO beep_channels (thread_id, thread_name, \
                            discord_user_id) VALUES ('{channel_id}','{channel_name}',\
                                                     '{discord_user_id}')"
                        await beep_chan_cursor.execute(insert_channels)
                        await beep_chan.commit()
                    elif result_1 is None and result_2 is not None:
                        discord.thread.delete()
                    else:
                        print("BEEPCH: Known channel")
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")


# async def update_url_imgs(aiohttp, BeautifulSoup, headers, branddb, channel, cursor, message):
#     grab_scodes = "SELECT style_code FROM shoes"
#     await cursor.execute(grab_scodes)
#     all_scodes = await cursor.fetchall()
#     print(f"UPURL: {all_scodes}")
#     all_scodes_list = [a for b in all_scodes for a in b]
#     print(f"UPURL: {all_scodes_list}")
#     for style_code in all_scodes_list:
#         # https: // www.google.com/imghp?hl = en & authuser = 0 & ogbl
#         query = "https://www.google.com/search?q={style_code}"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(query, headers=headers) as response:
#                 print(f"UPURL: {response.status}")
#                 if response.status == 200:
#                     text_content = await response.text()
#                     soup = BeautifulSoup(
#                         text_content,
#                         "html.parser")
#                     # print(f"UPURL: {soup}")
#                     found_image = soup.find("x22data:image").get_text()
#                     print(f"UPURL: {found_image}")
#                     add_img_url = f"UPDATE shoes SET image_url = '{found_image}' WHERE style_code \
# = '{style_code}'"
#                     await cursor.execute(add_img_url)
#     await branddb.commit()


async def msg_gif(aiohttp, GIPHY_TOKEN, channel, random, string):
    '''


    Parameters
    ----------
    aiohttp : TYPE
        DESCRIPTION.
    GIPHY_TOKEN : TYPE
        DESCRIPTION.
    channel : TYPE
        DESCRIPTION.
    random : TYPE
        DESCRIPTION.
    string : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q={string}&limit=10'
        ) as response:
            if response.status == 200:
                gifs_list = await response.json()
                gifs = gifs_list["data"]
                if gifs:
                    gif = random.choice(gifs)[
                        "url"]
                    gif_send = await channel.send(gif)
                    return await gif_send.delete(delay=10)


async def get_em(aiohttp, BeautifulSoup, bot, channel, add_shoe_channel, url):
    '''


    Parameters
    ----------
    aiohttp : TYPE
        DESCRIPTION.
    BeautifulSoup : TYPE
        DESCRIPTION.
    bot : TYPE
        DESCRIPTION.
    channel : TYPE
        DESCRIPTION.
    add_shoe_channel : TYPE
        DESCRIPTION.
    url : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    try:
        shoe_channel = bot.get_channel(add_shoe_channel)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                links = []
                image_links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.startswith('http') and ".com/t/" in href:
                        links.append(href)
                    if href.startswith('https://static') and href.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        image_links.append(href)
                        print(f"HERE: {image_links}")
                good_dict = {}
                good_d_list = []
                for d_link in links:
                    if d_link not in good_dict:
                        good_dict[d_link] = True
                        good_d_list.append(d_link)
                for good in good_d_list:
                    with open("bulk_add_list.txt", "r", encoding="utf-8") as bulk_r:
                        added_list = bulk_r.read().split("\n")
                        if good not in added_list:
                            site_send = await shoe_channel.send(good)
                            await site_send.delete(delay=5)
                            await asyncio.sleep(1)
                            with open("bulk_add_list.txt", "a", encoding="utf-8") as bulk_w:
                                bulk_w.write(f"{good}\n")
                await channel.send(f"{url} Done")
        await asyncio.sleep(1)
        if asyncio.current_task().cancelled():
            return
    except asyncio.CancelledError:
        print("Coroutine 1 was cancelled.")
