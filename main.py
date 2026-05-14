import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# =====================================
# НАСТРОЙКИ
# =====================================

BOT_TOKEN = "8670022200:AAFuOfkTAiOk_zQDeooEgyrjifURCIb0gCY"

CHAT_ID = 8670609815

# SSTATS API
API_HOST = "https://api.sstats.net"
ENDPOINT = f"{API_HOST}/Games/list"

API_KEY = "6tane6pbepb5wfto"

# =====================================
# BOT
# =====================================

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

# =====================================
# АНТИ-ДУБЛИ
# =====================================

sent_matches = set()

# =====================================
# ТОП ЛИГИ
# =====================================

TOP_LEAGUES = [
    "Premier League",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "Champions League",
    "Europa League",
    "World Cup",
    "Premier Liga"
]

# =====================================
# LIVE СКАНЕР
# =====================================

async def check_matches():

    while True:

        try:

            limit = 1000
            offset = 0

            all_matches = []

            while True:

                params = {
                    "Today": True,
                    "TimeZone": 3,
                    "limit": limit,
                    "offset": offset,
                    "apikey": API_KEY
                }

                async with aiohttp.ClientSession() as session:

                    async with session.get(
                        ENDPOINT,
                        params=params
                    ) as response:

                        if response.status != 200:

                            print(
                                "Ошибка API:",
                                response.status
                            )

                            break

                        result = await response.json()

                matches = result.get("data", [])

                if not matches:
                    break

                all_matches.extend(matches)

                offset += limit

            print(
                f"Получено матчей: "
                f"{len(all_matches)}"
            )

            for match in all_matches:

                try:

                    # ==================
                    # LIVE
                    # ==================

                    status = str(
                        match.get("Status", "")
                    ).lower()

                    if "live" not in status:
                        continue

                    # ==================
                    # МИНУТА
                    # ==================

                    minute = int(
                        match.get("Minute", 0)
                    )

                    if minute < 18 or minute > 35:
                        continue

                    # ==================
                    # ЛИГА
                    # ==================

                    league = str(
                        match.get("League", "")
                    )

                    if not any(
                        x.lower() in league.lower()
                        for x in TOP_LEAGUES
                    ):
                        continue

                    # ==================
                    # КОМАНДЫ
                    # ==================

                    home = match.get(
                        "HomeTeam",
                        "Home"
                    )

                    away = match.get(
                        "AwayTeam",
                        "Away"
                    )

                    # ==================
                    # СЧЕТ
                    # ==================

                    home_score = int(
                        match.get("HomeScore", 0)
                    )

                    away_score = int(
                        match.get("AwayScore", 0)
                    )

                    # максимум 1 гол
                    if (
                        home_score + away_score
                    ) > 1:
                        continue

                    # ==================
                    # ID
                    # ==================

                    match_id = (
                        f"{home}_{away}"
                    )

                    if match_id in sent_matches:
                        continue

                    sent_matches.add(match_id)

                    # ==================
                    # СИГНАЛ
                    # ==================

                    text = (
                        f"⚽ Football Goal AI\n\n"

                        f"🔥 LIVE сигнал\n\n"

                        f"🏆 {league}\n\n"

                        f"⚔️ {home} vs {away}\n\n"

                        f"📊 Счет:\n"
                        f"{home_score} - "
                        f"{away_score}\n\n"

                        f"⏱ Минута:\n"
                        f"{minute}\n\n"

                        f"🚨 Возможен гол "
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

# =====================================
# КОМАНДЫ
# =====================================

@dp.message(Command("start"))
async def start_cmd(message: types.Message):

    text = (
        "⚽ Football Goal AI\n\n"

        "🔥 LIVE сигналы "
        "на гол в 1 тайме\n\n"

        "⏱ Диапазон:\n"
        "18-35 минута\n\n"

        "🏆 ТОП лиги:\n"
        "🇬🇧 Англия\n"
        "🇩🇪 Германия\n"
        "🇪🇸 Испания\n"
        "🇫🇷 Франция\n"
        "🇮🇹 Италия\n"
        "🌍 Лига Чемпионов\n"
        "🌍 Лига Европы\n"
        "🌍 Чемпионат Мира\n\n"

        "📡 Бот работает 24/7"
    )

    await message.answer(text)

@dp.message(Command("status"))
async def status_cmd(message: types.Message):

    await message.answer(
        "🟢 LIVE сканирование активно"
    )

@dp.message(Command("signals"))
async def signals_cmd(message: types.Message):

    await message.answer(
        "🔥 Сигналы отправляются автоматически"
    )

@dp.message(Command("info"))
async def info_cmd(message: types.Message):

    await message.answer(
        "⚽ Football Goal AI\n\n"
        "📡 Анализ LIVE матчей\n"
        "🔥 Поиск голов "
        "в 1 тайме"
    )

# =====================================
# MAIN
# =====================================

async def main():

    asyncio.create_task(
        check_matches()
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)

if __name__ == "__main__":

    print("Football Goal AI started")

    asyncio.run(main())
