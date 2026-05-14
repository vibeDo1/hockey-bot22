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
            url = "https://api.sofascore.com/api/v1/sport/football/events/live"

            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            data = response.json()

            live_matches = data.get("events", [])

            print(f"LIVE матчей: {len(live_matches)}")

            for match in live_matches:

                try:
                    tournament = match["tournament"]["name"]

                    if not any(
                        league.lower() in tournament.lower()
                        for league in ALLOWED_LEAGUES
                    ):
                        continue

                    minute = match.get("time", {}).get("currentPeriodStartTimestamp")

                    home = match["homeTeam"]["name"]
                    away = match["awayTeam"]["name"]

                    score_home = match["homeScore"]["current"]
                    score_away = match["awayScore"]["current"]

                    match_id = str(match["id"])

                    if match_id in sent_matches:
                        continue

                    status = match.get("status", {}).get("description", "")

                    if "1st half" not in status.lower():
                        continue

                    # Берем только 18-35 минуту
                    current_time = match.get("time", {}).get("normaltime", 0)

                    if current_time < 18 or current_time > 35:
                        continue

                    text = f"""
⚽ Football Goal AI

🔥 LIVE сигнал на гол

🏆 {tournament}

⚔️ {home} vs {away}

📊 Счет:
{score_home} - {score_away}

⏱ Минута:
{current_time}

📈 Высокий темп игры
📡 LIVE матч
"""

                    await bot.send_message(CHAT_ID, text)

                    sent_matches.add(match_id)

                    print(f"Сигнал отправлен: {home} vs {away}")

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
