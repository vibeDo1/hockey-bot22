import asyncio
import requests
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = set()
sent_matches = set()

TOP_LEAGUES = [
    "Premier League",
    "Championship",
    "Bundesliga",
    "2. Bundesliga",
    "La Liga",
    "Ligue 1",
    "Ligue 2",
    "Premier Liga",
    "Serie A",
    "Eredivisie"
]


@dp.message(Command("start"))
async def start(message: Message):

    users.add(message.chat.id)

    await message.answer(
        "⚽ FOOTBALL LIVE BOT\n\n"
        "Бот ищет:\n"
        "• 18-35 минута\n"
        "• счет 0-0\n"
        "• сигнал на гол в 1 тайме 🔥"
    )


def get_live_matches():

    url = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

    try:

        response = requests.get(
            url,
            timeout=15
        )

        data = response.json()

        return data.get("events", [])

    except Exception as e:

        print("API ERROR:", e)

        return []


async def scanner():

    while True:

        try:

            matches = get_live_matches()

            print(f"Найдено матчей: {len(matches)}")

            for match in matches:

                try:

                    league = match.get(
                        "strLeague",
                        ""
                    )

                    if league not in TOP_LEAGUES:
                        continue

                    home = match.get(
                        "strHomeTeam",
                        ""
                    )

                    away = match.get(
                        "strAwayTeam",
                        ""
                    )

                    home_score = match.get(
                        "intHomeScore"
                    )

                    away_score = match.get(
                        "intAwayScore"
                    )

                    minute = match.get(
                        "strProgress",
                        "0"
                    )

                    if (
                        home_score is None
                        or
                        away_score is None
                    ):
                        continue

                    if (
                        int(home_score) != 0
                        or
                        int(away_score) != 0
                    ):
                        continue

                    try:

                        minute_int = int(minute)

                    except:

                        continue

                    if (
                        minute_int < 18
                        or
                        minute_int > 35
                    ):
                        continue

                    match_id = f"{home}-{away}"

                    if match_id in sent_matches:
                        continue

                    signal = (
                        f"⚽ ГОЛ В 1 ТАЙМЕ\n\n"
                        f"🏆 {league}\n\n"
                        f"{home} vs {away}\n\n"
                        f"⏱ Минута: {minute_int}\n"
                        f"📊 Счет: 0-0\n\n"
                        f"🔥 LIVE PRESSURE SIGNAL\n\n"
                        f"➡ ТБ 0.5 1 тайма"
                    )

                    for user_id in users:

                        try:

                            await bot.send_message(
                                user_id,
                                signal
                            )

                        except:
                            pass

                    sent_matches.add(match_id)

                    print("Сигнал отправлен")

                except Exception as e:

                    print("MATCH ERROR:", e)

            await asyncio.sleep(60)

        except Exception as e:

            print("SCAN ERROR:", e)

            await asyncio.sleep(60)


async def main():

    asyncio.create_task(scanner())

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
