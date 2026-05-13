import asyncio
import os
import aiohttp
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

URL = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

sent = set()

async def loop():

    async with aiohttp.ClientSession() as session:

        while True:

            try:

                async with session.get(
                    URL,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=20
                ) as response:

                    data = await response.json()

                for event in data.get("events", []):

                    try:

                        game_id = event["id"]

                        if game_id in sent:
                            continue

                        home = event["homeTeam"]["name"]
                        away = event["awayTeam"]["name"]

                        hs = event["homeScore"]["current"]
                        aw = event["awayScore"]["current"]

                        score = f"{hs}:{aw}"

                        if score not in ["1:0", "0:1"]:
                            continue

                        period = event.get("period", 1)

                        if period != 1:
                            continue

                        text = f"""
🚨 HOCKEY SIGNAL

🏒 {home} vs {away}

🥅 SCORE: {score}
"""

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text
                        )

                        sent.add(game_id)

                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)

            await asyncio.sleep(30)

asyncio.run(loop())
