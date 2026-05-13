import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

URL = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

sent = set()


# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def start_handler(message: types.Message):

    text = """
🏒 Добро пожаловать в Hockey Signals Bot

Бот автоматически ищет:
• завершённый 1 период
• счёт 1:0 или 0:1
• минимум 21 бросок в створ

После этого приходит сигнал 🚨
"""

    await message.answer(text)


# ===== ОСНОВНОЙ ЦИКЛ =====
async def hockey_loop():

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

                        # Только счёт 1:0 или 0:1
                        if score not in ["1:0", "0:1"]:
                            continue

                        # Проверка окончания 1 периода
                        period = event.get("period", 1)

                        # period == 2 означает:
                        # первый период завершён
                        if period != 2:
                            continue

                        stats = event.get("statistics", {})

                        shots_home = stats.get(
                            "shotsOnGoal", {}
                        ).get("home", 0)

                        shots_away = stats.get(
                            "shotsOnGoal", {}
                        ).get("away", 0)

                        total = shots_home + shots_away

                        # Минимум 21 бросок
                        if total < 21:
                            continue

                        text = f"""
🚨 HOCKEY SIGNAL

🏒 {home} vs {away}

🥅 SCORE AFTER 1ST PERIOD: {score}

📊 SHOTS ON GOAL: {total}

🔥 SIGNAL FOUND
"""

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text
                        )

                        sent.add(game_id)

                    except Exception as e:
                        print("EVENT ERROR:", e)

            except Exception as e:
                print("MAIN ERROR:", e)

            await asyncio.sleep(30)


# ===== ЗАПУСК =====
async def main():

    asyncio.create_task(hockey_loop())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())     
