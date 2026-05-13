import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8670022200:AAFuOfkTAiOk_zQDeooEgyrjifURCIb0gCY"

CHAT_ID = "8670609815"

bot = Bot(token=TOKEN)
dp = Dispatcher()

sent_matches = set()

TOP_LEAGUES = [
    "UEFA Champions League",
    "UEFA Europa League",
    "FIFA World Cup",
    "Premier League",
    "La Liga",
    "Bundesliga",
    "Ligue 1",
    "Serie A",
    "Russian Premier League"
]

@dp.message(Command("start"))
async def start(message: Message):
    text = """
⚽ Football Goal AI

🔥 LIVE сигналы на гол в 1 тайме

⏱ Диапазон:
18-35 минута

🏆 Лиги:
🇬🇧 Англия
🇩🇪 Германия
🇪🇸 Испания
🇫🇷 Франция
🇮🇹 Италия
🇷🇺 Россия
🌍 Лига Чемпионов
🌍 Лига Европы
🌍 Чемпионат Мира

📡 Бот работает 24/7
"""
    await message.answer(text)

async def scan_matches():
    while True:
        try:
            url = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

            response = requests.get(url).json()

            matches = response.get("events", [])

            for match in matches:

                league = str(match.get("strLeague", ""))
                minute = str(match.get("strProgress", "0"))

                home = match.get("strHomeTeam", "")
                away = match.get("strAwayTeam", "")

                if not home or not away:
                    continue

                title = f"{home} vs {away}"

                if not any(top in league for top in TOP_LEAGUES):
                    continue

                try:
                    minute_int = int(minute)
                except:
                    continue

                if minute_int < 18 or minute_int > 35:
                    continue

                match_id = f"{title}_{minute}"

                if match_id in sent_matches:
                    continue

                sent_matches.add(match_id)

                text = f"""
🚨 LIVE SIGNAL 🚨

⚽ {title}

🏆 {league}

⏱ Минута: {minute_int}

🔥 Сигнал:
ГОЛ В 1 ТАЙМЕ

📈 Football Goal AI
"""

                await bot.send_message(CHAT_ID, text)

            await asyncio.sleep(60)

        except Exception as e:
            print(e)
            await asyncio.sleep(30)

async def main():
    asyncio.create_task(scan_matches())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
