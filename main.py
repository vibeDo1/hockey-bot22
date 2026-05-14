import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = "8652395156:AAEfEMjPY6sfE1JIDwzh-PY6H8VkNsVXwo2k"

CHAT_ID = 8670609815

API_KEY = "6tane6pbepb5wfto"

# =========================
# BOT
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

sent_matches = set()

# =========================
# LIVE ПРОВЕРКА МАТЧЕЙ
# =========================

async def check_matches():

    url = "https://api.sstats.net/v1/football/fixtures/live"

    headers = {
        "X-API-Key": API_KEY
    }

    while True:

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    url,
                    headers=headers
                ) as response:

                    if response.status != 200:
                        print("Ошибка API:", response.status)
                        await asyncio.sleep(60)
                        continue

                    data = await response.json()

                    matches = data.get("data", [])

                    print(f"Найдено LIVE матчей: {len(matches)}")

                    for match in matches:

                        try:

                            minute = int(
                                match.get("minute", 0)
                            )

                            # Только 18-35 минута
                            if minute < 18 or minute > 35:
                                continue

                            home = match.get(
                                "home_name",
                                "Home"
                            )

                            away = match.get(
                                "away_name",
                                "Away"
                            )

                            league = match.get(
                                "competition_name",
                                "League"
                            )

                            score = match.get(
                                "score",
                                "0:0"
                            )

                            match_id = (
                                f"{home}_{away}_{minute}"
                            )

                            # Защита от повторов
                            if match_id in sent_matches:
                                continue

                            sent_matches.add(match_id)

                            text = (
                                f"🔥 LIVE СИГНАЛ\n\n"
                                f"⚽ {home} vs {away}\n"
                                f"🏆 {league}\n"
                                f"⏱ {minute} минута\n"
                                f"📊 Счёт: {score}\n\n"
                                f"🚨 Возможен гол в 1 тайме"
                            )

                            await bot.send_message(
                                chat_id=CHAT_ID,
                                text=text
                            )

                            print(
                                f"Сигнал отправлен: "
                                f"{home} vs {away}"
                            )

                        except Exception as e:
                            print("Ошибка матча:", e)

            await asyncio.sleep(60)

        except Exception as e:
            print("Ошибка API:", e)
            await asyncio.sleep(60)

# =========================
# КОМАНДА START
# =========================

@dp.message(Command("start"))
async def start_cmd(message: types.Message):

    text = (
        "⚽ Football Goal AI\n\n"
        "🔥 LIVE сигналы на гол "
        "в 1 тайме\n\n"

        "⏱ Диапазон:\n"
        "18-35 минута\n\n"

        "🏆 Лиги:\n"
        "🇬🇧 Англия\n"
        "🇩🇪 Германия\n"
        "🇪🇸 Испания\n"
        "🇫🇷 Франция\n"
        "🇮🇹 Италия\n"
        "🇷🇺 Россия\n"
        "🌍 Лига Чемпионов\n"
        "🌍 Лига Европы\n"
        "🌍 Чемпионат Мира\n\n"

        "📡 Бот работает 24/7"
    )

    await message.answer(text)

# =========================
# КОМАНДА INFO
# =========================

@dp.message(Command("info"))
async def info_cmd(message: types.Message):

    text = (
        "ℹ️ Football Goal AI\n\n"

        "Бот автоматически ищет\n"
        "LIVE матчи и отправляет\n"
        "сигналы на возможный гол.\n\n"

        "✅ Только реальные LIVE матчи\n"
        "✅ Проверка каждые 60 секунд\n"
        "✅ Диапазон 18-35 минут"
    )

    await message.answer(text)

# =========================
# КОМАНДА STATUS
# =========================

@dp.message(Command("status"))
async def status_cmd(message: types.Message):

    await message.answer(
        "🟢 Бот активен и работает 24/7"
    )

# =========================
# MAIN
# =========================

async def main():

    asyncio.create_task(
        check_matches()
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
