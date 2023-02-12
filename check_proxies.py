'''queue the proxies'''
import queue
import os
import time
import requests
from bs4 import BeautifulSoup

q= queue.Queue()
headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
modified_file_time = os.path.getmtime("valid_proxies.txt")
now_time = time.time()
free_page = requests.get("https://free-proxy-list.net/", headers= headers, timeout=1)
ssl_page = requests.get("http://www.sslproxies.org",  headers= headers, timeout=1)
new_proxies = BeautifulSoup(free_page.content, 'html.parser')
current_new_proxies = new_proxies.find("textarea", {"class":"form-control"}).get_text()
new_ssl = BeautifulSoup(ssl_page.content, 'html.parser')
current_new_ssl = new_ssl.find("textarea", {"class":"form-control"}).get_text()

def fresh_proxies():
    with open("proxy_list.txt", "w") as pl:
        if now_time - modified_file_time > 540:
            fresh_proxie = current_new_proxies[75:]
            fresh_ssl = current_new_ssl[75:]
            pl.write(fresh_proxie)
            pl.write(fresh_ssl)
            print("Done adding fresh proxies")
            check_proxies()
            pl.close()

def check_proxies():
    '''make sure the proxies are working'''
    # if now_time - modified_file_time > 540:
    with open("proxy_list.txt", "r") as f:
        proxies = f.read().split('\n')
        for p in proxies:
            q.put(p)


    valid_proxies = []
    print("Begin Check")
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                                proxies={"http": proxy, "https:": proxy}, timeout = 1)
            if res.status_code == 200:
                print(proxy + " valid and added")
                valid_proxies.append(proxy)
        except:
            continue
        finally:
            print("wompwomp")
    with open("valid_proxies.txt", "w") as v:
        vps = " \n".join(valid_proxies)
        v.write(vps)
        print("done validating proxies")

