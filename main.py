import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

URL = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

sent_games = set()


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🏒 Хоккейный бот работает\n\n"
        "Сигналы будут приходить автоматически."
    )


async def scanner():

    await asyncio.sleep(5)

    async with aiohttp.ClientSession() as session:

        while True:

            try:

                async with session.get(
                    URL,
                    headers={"User-Agent": "Mozilla/5.0"}
                ) as response:

                    data = await response.json()

                    events = data.get("events", [])

                    print(f"Найдено матчей: {len(events)}")

                    for event in events:

                        try:

                            game_id = str(event["id"])

                            if game_id in sent_games:
                                continue

                            home = event["homeTeam"]["name"]
                            away = event["awayTeam"]["name"]

                            home_score = event["homeScore"]["current"]
                            away_score = event["awayScore"]["current"]

                            score = f"{home_score}:{away_score}"

                            # нужен счет 1:0 или 0:1
                            if score not in ["1:0", "0:1"]:
                                continue

                            # закончился 1 период
                            status = event.get("status", {})

                            period = status.get("period", 0)

                            if period != 1:
                                continue

                            description = status.get("description", "")

                            if "Break" not in description and "Pause" not in description:
                                continue

                            text = (
                                f"🚨 HOCKEY SIGNAL\n\n"
                                f"🏒 {home} vs {away}\n\n"
                                f"🥅 Счет: {score}\n"
                                f"⏱ Конец 1 периода"
                            )

                            await bot.send_message(
                                chat_id=CHAT_ID,
                                text=text
                            )

                            print("Сигнал отправлен")

                            sent_games.add(game_id)

                        except Exception as e:
                            print("Ошибка матча:", e)

            except Exception as e:
                print("Ошибка сканера:", e)

            await asyncio.sleep(30)


async def main():

    asyncio.create_task(scanner())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
