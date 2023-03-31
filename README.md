# BeepBoopBot
Pythong, MySQL, Discord API, GIPHY API, TENOR API, OPENAI API Practice Project

    This is a fun project, creating a discord bot that catalogs product links and checks them for
new information on command.  Also integrated some simple ChatGPT functionality into the bot for 
kicks initially.
    Using MAMP I created a few MySQL databases to handle the information the bot receives and to
catalog the links and their information.  You can add a new site into a particular url format
category, then add links of products from that url to be cataloged.  Using multiple commands you
can retrieve the info on the item or items and check the price depending on the policy of the
website.  The bot will create channels if the discord does not have the appropriate ones, keep
itself tidy by erasing prompt or notification messages it sends, store ChatGPT conversation to be
learned by the bot later and more!
    Users create their own private threads through chat prompts to access the major functionalities
of the bot.  Commands are restricted based on channels and roles.  Each thread has a pinned message
with reactions loaded for click access to functions or function instructions.  All reaction
functions self erase as well.

Functionality:
👀 : SITE LIST
👟 : SHOE LIST
💵 : FIND STYLE
🧹 : CLEAR
👍🏾 : ADD SITE
👎🏾 : DEL SITE
📚 : ADD SHOE 
🌪️ : REFRESH
🔍 : GIMME
🤬 : COMMANDS
❓ : HELP

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

    There are a few dependencies that need to be setup, for instance creating a few labeled empty text
    files and loading the appropriate environment variables.


