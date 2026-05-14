import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "ТВОЙ_ТОКЕН"

CHAT_ID = 8670609815

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

sent_matches = set()

ALLOWED_LEAGUES = [
    "Premier League",
    "Champions League",
    "Europa League",
    "LaLiga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "World Cup",
    "Premier Liga"
]


async def scan_live_matches():
    while True:
        try:
            url = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"

            response = requests.get(url).json()

            events = response.get("events", [])

            print(f"LIVE матчей: {len(events)}")

            for event in events:

                try:
                    competition = event["competitions"][0]

                    status = competition["status"]["type"]["description"]

                    # Только LIVE
                    if "Half" not in status and "minute" not in status.lower():
                        continue

                    details = competition["status"]["displayClock"]

                    try:
                        minute = int(details.replace("'", ""))
                    except:
                        continue

                    # Только 18-35 минута
                    if minute < 18 or minute > 35:
                        continue

                    home = competition["competitors"][0]["team"]["displayName"]
                    away = competition["competitors"][1]["team"]["displayName"]

                    home_score = competition["competitors"][0]["score"]
                    away_score = competition["competitors"][1]["score"]

                    league = event["league"]["name"]

                    match_id = event["id"]

                    if match_id in sent_matches:
                        continue

                    text = f"""
⚽ Football Goal AI

🔥 LIVE сигнал на гол

🏆 {league}

⚔️ {home} vs {away}

📊 Счет:
{home_score} - {away_score}

⏱ Минута:
{minute}

📡 Реальный LIVE матч
"""

                    await bot.send_message(CHAT_ID, text)

                    sent_matches.add(match_id)

                    print(f"Отправлен сигнал: {home} vs {away}")

                except Exception as e:
                    print("Ошибка матча:", e)

        except Exception as e:
            print("Ошибка API:", e)

        await asyncio.sleep(60)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "⚽ Football Goal AI\n\n"
        "🔥 LIVE сигналы на гол в 1 тайме\n"
        "⏱ Диапазон: 18-35 минута\n"
        "📡 Бот работает 24/7"
    )


@dp.message(Command("status"))
async def status_cmd(message: types.Message):
    await message.answer(
        "✅ Бот активен\n📡 LIVE сканирование работает"
    )


@dp.message(Command("signals"))
async def signals_cmd(message: types.Message):
    await message.answer(
        "🔥 Сигналы отправляются автоматически"
    )


@dp.message(Command("info"))
async def info_cmd(message: types.Message):
    await message.answer(
        "🤖 Football Goal AI\n"
        "⚽ LIVE анализ матчей\n"
        "🔥 Сигналы на гол"
    )


async def main():
    asyncio.create_task(scan_live_matches())
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started")
    asyncio.run(main())
