"""
Beep content checker

"""


async def find_style_code(aiohttp,
                          BeautifulSoup,
                          asyncio,
                          random,
                          headers_rotate,
                          message,
                          home_channel,
                          channel,
                          cursor,
                          branddb):

    """
    # price checking

    """
    if message.channel.id == home_channel:
        strip_m = message.content[10:]
        strip_mess = strip_m.strip(" ").split(",")
        print(strip_mess)
        style_c = ("SELECT style_code FROM shoes")
        await cursor.execute(style_c)
        style_code_table_array = [a for b in await cursor.fetchall() for a in b]
        for scode in strip_mess:
            # message_length = len(message.content[10:].split(","))
            if scode in style_code_table_array:
                print("Looping for style code:", scode)
                # shoe = ("SELECT name FROM shoes WHERE style_code = %s") #change brand to model
                # cursor.execute(shoe, (scode))
                # shoe_sc_found = cursor.fetchall()
                sc_urls = ("SELECT url FROM shoes WHERE style_code = %s")
                await cursor.execute(sc_urls, (scode))
                # URL = ', '.join(sc_url_list)
                sc_urls_fet = await cursor.fetchall()
                sc_url_list = [a for b in sc_urls_fet for a in b]
                # shoe_sc = [a for b in shoe_sc_found for a in b]
                # shoe_code_list = '\n'.join(shoe_sc.replace("-", " "))
                # await channel.send(sc_url_list)
                for s in sc_url_list:
                    # await channel.send(s)
                    with open("valid_proxies.txt", "r", encoding="utf-8") as vp:
                        await channel.send("spinning")
                        try:
                            success = False
                            if "www.nike.com" in s.lower():
                                await channel.send(scode + " it nike")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as nike_session:
                                        async with nike_session.get(s) as response:
                                            # print(response)
                                            # print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content,
                                                    "html.parser")
                                                nike_current_price = soup.find(
                                                    "div", {
                                                        "class": "product-price css-11s12ax is--current-price css-tpaepq"
                                                    }).get_text()
                                                # await channel.send(nike_current_price)
                                                nike_color = soup.find(
                                                    "li", {
                                                        "class": "description-preview__color-description ncss-li"
                                                    }).get_text()
                                                nike_color = nike_color.split(
                                                    ":").pop(-1)
                                                # await channel.send(nike_color)
                                                print("1")
                                                color_query = f"UPDATE shoes SET color =\
                                                    '{nike_color}' WHERE url = '{s}'"
                                                await cursor.execute(color_query)
                                                price_query = f"SELECT price FROM shoes WHERE url =\
                                                    '{s}'"
                                                await cursor.execute(price_query)
                                                price_q = await cursor.fetchone()
                                                print("2")
                                                # await channel.send(price_q)
                                                if price_q[0] == None:
                                                    insert_query = f"UPDATE shoes SET price =\
                                                        '{nike_current_price}' WHERE url = '{s}'"
                                                else:
                                                    # await channel.send(price_q[0])
                                                    insert_query = f"UPDATE shoes SET current_price\
                                                        = '{nike_current_price}' WHERE url = '{s}'"
                                                await cursor.execute(insert_query)
                                                print("3")
                                                await branddb.commit()
                                                await channel.send(f"current {nike_current_price}\
                                                                   old {price_q}")
                                                await channel.send(s)
                                                break
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                print("4")
                                                break

                            elif "www.footlocker.com" in s.lower():
                                await channel.send(scode + " it footlocker")
                                new_s = s.split('/').pop(4)
                                print(new_s)
                                fl_s = s.replace(new_s, "~")
                                print(fl_s)
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as fl_session:
                                        async with fl_session.get(fl_s, headers=headers_rotate
                                                                  ) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                print("1")
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                fl_current_price = soup.find(
                                                    "span", {"class": "ProductPrice"}).get_text()
                                                print("2")
                                                insert_query = (
                                                    f"UPDATE shoes SET price =\
                                                        '{fl_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(fl_current_price)
                                                await channel.send(fl_s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                print("5")
                                                break

                            elif "www.dickssportinggoods.com" in s.lower():
                                await channel.send(scode + " it dicks")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as dicks_session:
                                        async with dicks_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                dicks_current_price = soup(
                                                    "span", {
                                                        "class": "product-price ng-star-inserted"
                                                    }).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price =\
                                                        '{dicks_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(dicks_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "www.nordstrom.com" in s.lower():
                                await channel.send(scode + " it nordstrom")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as nord_session:
                                        async with nord_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')

                                                nord_current_price = soup.find(
                                                    'div', {
                                                        'class': 'ggbBg y3xFi'
                                                    }).get_text
                                                nord_current_price['aria-hidden'] = 'false'
                                                insert_query = (
                                                    f"UPDATE shoes SET price =\
                                                        '{nord_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(nord_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "www.mrporter.com" in s.lower():
                                await channel.send(scode + " it mrporter")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as mrp_session:
                                        async with mrp_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                mrp_current_price = soup.find(
                                                    "span", {"itemprop": "price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price =\
                                                        '{mrp_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                await branddb.commit()
                                                await channel.send(mrp_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "www.finishline.com" in s.lower():
                                await channel.send(scode + " it finishline")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as fin_session:
                                        async with fin_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                finish_current_price = soup.find(
                                                    "div", {"class": "productPrice"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price =\
                                                        '{finish_current_price}'\
                                                            WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(finish_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "www.footpatrol.com" in s.lower():
                                await channel.send(scode + " it footpatrol")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as foot_p_session:
                                        async with foot_p_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                footpatrol_current_price = soup.find(
                                                    "span", {"data-e2e":
                                                             "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = \
                                                        '{footpatrol_current_price}\
                                                            ' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(footpatrol_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "thehipstore.co.uk" in s.lower():
                                await channel.send(scode + " it hipstore")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as hip_session:
                                        async with hip_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                hips_current_price = soup.find(
                                                    "span", {
                                                        "data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = \
                                                        '{hips_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(hips_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break

                            elif "size.co.uk" in s.lower():
                                await channel.send(scode + " it size.co")
                                await channel.send("spinning")
                                for proxy in vp:
                                    # try:
                                    print(
                                        f"using the proxy: {proxy.strip()}")
                                    async with aiohttp.ClientSession() as size_session:
                                        async with size_session.get(s) as response:
                                            print(response)
                                            print(response.status)
                                            if response.status == 200:
                                                success = True
                                                text_content = await response.text()
                                                soup = BeautifulSoup(
                                                    text_content, 'html.parser')
                                                size_current_price = soup.find(
                                                    "span", {
                                                        "data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = \
                                                        '{size_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(size_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                if response.status == 403:
                                                    print("No Access")
                                                    await channel.send("Blocked")
                                                    break
                                                else:
                                                    print(
                                                        "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success == True:
                                                break
                            else:
                                await channel.send(f"{s} \n Na son, cloudfare\n")
                        except print("beep price failed"):
                            continue
                    await channel.send("Done")
