# BeepBoopBot
Practice Project

    This is a fun project, creating a discord bot that catalogs product links and checks them for
new information on command.  Also integrated ChatGPT into the bot for fun.  Using MAMP I created
a few MySQL databases to handle the information the bot receives and to catalog the links and
their information.  You can add a new site into a particular url format category, then add links
of products from that url to be cataloged.  Using multiple commands you can retrieve the info
on the item or items and check the price depending on the policy of the website.  The bot will
create channels if the discord does not have the appropriate ones, keep itself tidy by erasing
prompt or notification messages it sends, store ChatGPT conversation to be learned by the bot
later and more!

    I acheived this using these libraries:

Python Lib

aiohttp, aiofiles, aioMySql
asyncio, nest_asyncio
----
For asynchronous functions 

discord.py
----
Discord API

openai
----
OpenAI ChatGPT API

BeautifulSoup
----
For scraping

Python dotenv
----
For security

    There are a few dependencies that need to be setup, for instance creating the empty text
    files and loading the appropriate environment variables.


