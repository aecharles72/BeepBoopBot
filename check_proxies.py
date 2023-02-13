# '''queue the proxies'''
# import queue
import aiohttp
import aiofiles
import asyncio
import nest_asyncio
import os
import time
import random
import requests
from bs4 import BeautifulSoup

nest_asyncio.apply()

# q= queue.Queue()

headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

modified_file_time = os.path.getmtime("valid_proxies.txt")
now_time = time.time()

free_page = requests.get("https://free-proxy-list.net/", headers= headers, timeout=1)
ssl_page = requests.get("http://www.sslproxies.org",  headers= headers, timeout=1)
new_proxies = BeautifulSoup(free_page.content, 'html.parser')
current_new_proxies = new_proxies.find("textarea", {"class":"form-control"}).get_text()
new_ssl = BeautifulSoup(ssl_page.content, 'html.parser')
current_new_ssl = new_ssl.find("textarea", {"class":"form-control"}).get_text()

async def fresh_proxies():
   async with aiofiles.open("proxy_list.txt", "w") as pl:
       print(now_time)
       print(modified_file_time)
       if now_time - modified_file_time > 540:
           fresh_proxie = current_new_proxies[75:]
           # fresh_ssl = current_new_ssl[75:]
           await pl.write(fresh_proxie)
           # await pl.write(fresh_ssl)
           print("Done adding fresh proxies")
           pl.close()


async def check_proxies():
    async with aiofiles.open("proxy_list.txt", "r") as f:
        proxies = await ''.join(f.read()).split()
        valid_proxies = []
        async with aiohttp.ClientSession() as session:
            for proxy in proxies:
                print(proxy)
                try:
                    async with session.get("http://ipinfo.io/json") as res:
                        print(res.status)
                        if res.status == 200:
                            valid_proxies.append(proxy)
                            await asyncio.sleep(random.uniform(1, 5))
                except:
                    continue

    async with aiofiles.open("valid_proxies.txt", "w") as v:
        await v.write("\n".join(valid_proxies))
