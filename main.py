import asyncio
import os
import requests
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

URL = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

sent = set()

async def loop():

    while True:

        try:

            response = requests.get(
                URL,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=20
            )

            data = response.json()

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

                    stats = event.get("statistics", {})

                    shots_home = stats.get(
                        "shotsOnGoal", {}
                    ).get("home", 0)

                    shots_away = stats.get(
                        "shotsOnGoal", {}
                    ).get("away", 0)

                    total = shots_home + shots_away

                    if total < 21:
                        continue

                    text = f"""
🚨 HOCKEY SIGNAL

🏒 {home} vs {away}

🥅 SCORE: {score}

📊 SHOTS: {total}

🔥 SIGNAL: YES
"""

                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=text
                    )

                    sent.add(game_id)

                except Exception:
                    continue

        except Exception as e:
            print(e)

        await asyncio.sleep(30)

asyncio.run(loop())
