# -*- coding: utf-8 -*-
# price checking
async def find_style_code(aiohttp, BeautifulSoup, asyncio, random, message, channel, cursor, branddb):
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
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
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
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
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
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
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
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break

                        elif "www.mrporter.com" in s.lower():
                            await channel.send(scode + " it mrporter")
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
                                                mrp_current_price = soup.find(
                                                    "span", {"itemprop": "price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{mrp_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(mrp_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break

                        elif "www.finishline.com" in s.lower():
                            await channel.send(scode + " it finishline")
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
                                                finish_current_price = soup.find(
                                                    "div", {"class": "productPrice"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{finish_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(finish_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break

                        elif "www.footpatrol.com" in s.lower():
                            await channel.send(scode + " it footpatrol")
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
                                                footpatrol_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{footpatrol_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(footpatrol_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break

                        elif "thehipstore.co.uk" in s.lower():
                            await channel.send(scode + " it hipstore")
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
                                                hips_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{hips_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(hips_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break

                        elif "size.co.uk" in s.lower():
                            await channel.send(scode + " it size.co")
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
                                                size_current_price = soup.find(
                                                    "span", {"data-e2e": "product-price"}).get_text()
                                                insert_query = (
                                                    f"UPDATE shoes SET price = '{size_current_price}' WHERE url = '{s}';")
                                                cursor.execute(
                                                    insert_query)
                                                branddb.commit()
                                                await channel.send(size_current_price)
                                                await channel.send(s)
                                            else:
                                                print(response.status)
                                                print(
                                                    "damn, might wanna refresh the proxies")
                                                await asyncio.sleep(random.uniform(1, 5))
                                                continue
                                            if success:
                                                break
                        else:
                            await channel.send(f"{s} \n Na son, cloudfare\n")
                    except:
                        continue
                await channel.send("Done")
