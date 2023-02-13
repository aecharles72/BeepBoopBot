import asyncio
import aiohttp
import random
import time
from bs4 import BeautifulSoup

# Define a list of user-agent strings to randomly select from
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4763.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
]


async def get_nike_price(session):
    url = "https://www.nike.com/t/air-max-2090-sneaker-g9ZjK1"
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    async with session.get(url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        price = soup.find("span", class_="css-kodz8g").get_text().strip()
        return price
    price = await get_nike_price(session)
    await channel.send(price)
    await asyncio.sleep(random.uniform(1, 5))


async def main():
    async with aiohttp.ClientSession() as session:
        price = await get_nike_price(session)
        print(price)
        # Add a random delay to avoid detection
        await asyncio.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    asyncio.run(main())
