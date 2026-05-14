import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "8670022200:AAFuOfkTAiOk_zQDeooEgyrjifURCIb0gCY"

CHAT_ID = 8670609815

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

sent_matches = set()

LEAGUES = [
    "Premier League",
    "Champions League",
    "Europa League",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "World Cup",
    "Russian Premier League"
]


async def scan_matches():
    while True:
        try:
            url = "https://www.scorebat.com/video-api/v3/"
            response = requests.get(url).json()

            matches_found = 0

            for item in response.get("response", []):

                title = item.get("title", "")
                competition = item.get("competition", "")
                match_id = item.get("matchviewUrl", "")

                if match_id in sent_matches:
                    continue

                if not any(l.lower() in competition.lower() for l in LEAGUES):
                    continue

                live_words = ["live", "1st half", "first half"]

                if not any(w.lower() in title.lower() for w in live_words):
                    continue

                matches_found += 1

                text = f"""
⚽ Football Goal AI

🔥 LIVE сигнал на гол

🏆 {competition}

⚔️ {title}

⏱ Время матча:
18-35 минута

📈 Высокий темп игры
📡 LIVE матч

"""

                await bot.send_message(CHAT_ID, text)

                sent_matches.add(match_id)

            print(f"Найдено матчей: {matches_found}")

        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(60)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    text = """
⚽ Football Goal AI

🔥 LIVE сигналы на гол в 1 тайме

⏱ Диапазон:
18–35 минута

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


@dp.message(Command("status"))
async def status_cmd(message: types.Message):
    await message.answer(
        "✅ Бот активен\n📡 LIVE сканирование работает"
    )


@dp.message(Command("signals"))
async def signals_cmd(message: types.Message):
    await message.answer(
        "🔥 LIVE сигналы отправляются автоматически при обнаружении сильного матча"
    )


@dp.message(Command("info"))
async def info_cmd(message: types.Message):
    await message.answer(
        "🤖 Football Goal AI\n\n"
        "⚽ Анализ LIVE матчей\n"
        "🔥 Сигналы на гол в 1 тайме\n"
        "⏱ Интервал: 18-35 минута\n"
        "📡 Работа 24/7"
    )


async def main():
    asyncio.create_task(scan_matches())
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started")
    asyncio.run(main())
