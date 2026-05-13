import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

URL = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

sent_games = set()

# КНОПКИ

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статус")],
        [KeyboardButton(text="🏒 Live матчи")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True
)


# START

@dp.message(Command("start"))
async def start_cmd(message: Message):

    text = (
        "🏒 HOCKEY SIGNAL BOT\n\n"
        "Бот отслеживает live хоккейные матчи.\n\n"
        "📡 Сигналы приходят автоматически."
    )

    await message.answer(
        text,
        reply_markup=keyboard
    )


# STATUS

@dp.message(lambda message: message.text == "📊 Статус")
async def status_handler(message: Message):

    await message.answer(
        "✅ Бот работает\n"
        "📡 Сканер активен\n"
        "⏱ Проверка каждые 30 секунд"
    )


# HELP

@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def help_handler(message: Message):

    await message.answer(
        "ℹ️ Бот ищет хоккейные матчи:\n\n"
        "• счет 1:0 или 0:1\n"
        "• конец 1 периода\n"
        "• live матчи SofaScore"
    )


# LIVE MATCHES

@dp.message(lambda message: message.text == "🏒 Live матчи")
async def games_handler(message: Message):

    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(
                URL,
                headers={"User-Agent": "Mozilla/5.0"}
            ) as response:

                data = await response.json()

                events = data.get("events", [])

                if not events:
                    await message.answer("❌ Live матчей нет")
                    return

                text = "🏒 LIVE МАТЧИ\n\n"

                for event in events[:10]:

                    home = event["homeTeam"]["name"]
                    away = event["awayTeam"]["name"]

                    hs = event["homeScore"]["current"]
                    aw = event["awayScore"]["current"]

                    text += f"{home} {hs}:{aw} {away}\n"

                await message.answer(text)

    except Exception as e:

        await message.answer(f"Ошибка: {e}")


# СКАНЕР

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

                            hs = event["homeScore"]["current"]
                            aw = event["awayScore"]["current"]

                            score = f"{hs}:{aw}"

                            if score not in ["1:0", "0:1"]:
                                continue

                            status = event.get("status", {})

                            period = status.get("period", 0)

                            if period != 1:
                                continue

                            description = status.get(
                                "description",
                                ""
                            )

                            if (
                                "Break" not in description
                                and
                                "Pause" not in description
                            ):
                                continue

                            text = (
                                f"🚨 HOCKEY SIGNAL\n\n"
                                f"🏒 {home} vs {away}\n\n"
                                f"🥅 Счет: {score}\n"
                                f"⏱ Конец 1 периода\n\n"
                                f"🔥 SIGNAL"
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


# MAIN

async def main():

    asyncio.create_task(scanner())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
