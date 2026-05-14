import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ======================================
# НАСТРОЙКИ
# ======================================

BOT_TOKEN = "8670022200:AAFuOfkTAiOk_zQDeooEgyrjifURCIb0gCY"

CHAT_ID = 8670609815

API_KEY = "6tane6pbepb5wfto"

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

# ======================================
# АНТИ-ДУБЛИ
# ======================================

sent_matches = set()

# ======================================
# ТОП ЛИГИ
# ======================================

TOP_LEAGUES = [
    "Premier League",
    "Bundesliga",
    "La Liga",
    "Serie A",
    "Ligue 1",
    "Champions League",
    "Europa League",
    "World Cup",
    "Premier Liga"
]

# ======================================
# LIVE СКАНЕР
# ======================================

async def scan_live_matches():

    while True:

        try:

            url = (
                "https://api.sstats.net/football/games"
            )

            headers = {
                "X-API-Key": API_KEY
            }

            params = {
                "status": "live"
            }

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=20
                ) as response:

                    data = await response.json()

            matches = data.get("data", [])

            print(f"LIVE матчей: {len(matches)}")

            for match in matches:

                try:

                    # ======================
                    # МИНУТА
                    # ======================

                    minute = int(
                        match.get("minute", 0)
                    )

                    if minute < 18 or minute > 35:
                        continue

                    # ======================
                    # ЛИГА
                    # ======================

                    league = str(
                        match.get("league", "")
                    )

                    if not any(
                        x.lower() in league.lower()
                        for x in TOP_LEAGUES
                    ):
                        continue

                    # ======================
                    # КОМАНДЫ
                    # ======================

                    home = match.get(
                        "home_name",
                        "Home"
                    )

                    away = match.get(
                        "away_name",
                        "Away"
                    )

                    # ======================
                    # СЧЕТ
                    # ======================

                    home_score = int(
                        match.get("home_score", 0)
                    )

                    away_score = int(
                        match.get("away_score", 0)
                    )

                    # максимум 1 гол
                    if home_score + away_score > 1:
                        continue

                    # ======================
                    # ОПАСНЫЕ АТАКИ
                    # ======================

                    dangerous_home = int(
                        match.get(
                            "dangerous_attacks_home",
                            0
                        )
                    )

                    dangerous_away = int(
                        match.get(
                            "dangerous_attacks_away",
                            0
                        )
                    )

                    # минимум давление
                    if (
                        dangerous_home < 20
                        and dangerous_away < 20
                    ):
                        continue

                    # ======================
                    # ID
                    # ======================

                    match_id = str(
                        match.get("id")
                    )

                    if match_id in sent_matches:
                        continue

                    sent_matches.add(match_id)

                    # ======================
                    # СИГНАЛ
                    # ======================

                    text = (
                        f"⚽ Football Goal AI\n\n"
                        f"🔥 LIVE сигнал\n\n"
                        f"🏆 {league}\n\n"
                        f"⚔️ {home} vs {away}\n\n"
                        f"📊 Счет:\n"
                        f"{home_score} - {away_score}\n\n"
                        f"⏱ Минута: {minute}\n\n"
                        f"📈 Опасные атаки:\n"
                        f"{dangerous_home} - "
                        f"{dangerous_away}\n\n"
                        f"🔥 Возможен гол "
                        f"в 1 тайме"
                    )

                    await bot.send_message(
                        CHAT_ID,
                        text
                    )

                    print(
                        f"Сигнал отправлен: "
                        f"{home} vs {away}"
                    )

                except Exception as e:

                    print(
                        "Ошибка матча:",
                        e
                    )

        except Exception as e:

            print(
                "Ошибка API:",
                e
            )

        await asyncio.sleep(60)

# ======================================
# КОМАНДЫ
# ======================================

@dp.message(Command("start"))
async def start_cmd(message: types.Message):

    text = (
        "⚽ Football Goal AI\n\n"
        "🔥 LIVE сигналы "
        "на гол в 1 тайме\n\n"
        "⏱ Диапазон:\n"
        "18-35 минута\n\n"
        "📡 Бот работает 24/7"
    )

    await message.answer(text)

@dp.message(Command("status"))
async def status_cmd(message: types.Message):

    await message.answer(
        "✅ LIVE сканирование активно"
    )

@dp.message(Command("signals"))
async def signals_cmd(message: types.Message):

    await message.answer(
        "🔥 Сигналы отправляются автоматически"
    )

@dp.message(Command("info"))
async def info_cmd(message: types.Message):

    await message.answer(
        "⚽ Football Goal AI\n"
        "📡 Анализ LIVE матчей\n"
        "🔥 Поиск голов в 1 тайме"
    )

# ======================================
# ЗАПУСК
# ======================================

async def main():

    asyncio.create_task(
        scan_live_matches()
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)

if __name__ == "__main__":

    print("Football Goal AI started")

    asyncio.run(main())
