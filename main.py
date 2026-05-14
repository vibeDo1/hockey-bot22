import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ====================================
# НАСТРОЙКИ
# ====================================

TOKEN = "8670022200:AAFuOfkTAiOk_zQDeooEgyrjifURCIb0gCY"

CHAT_ID = "8670609815"

API_KEY = "6tane6pbepb5wfto"

bot = Bot(token=TOKEN)

dp = Dispatcher()

# ====================================
# АНТИ-ДУБЛИ
# ====================================

sent_matches = set()

# ====================================
# ТОП ЛИГИ
# ====================================

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

# ====================================
# LIVE СКАНЕР
# ====================================

async def scan_live_matches():

    while True:

        try:

            url = (
                f"https://api.sstats.net/games?"
                f"apikey={API_KEY}"
            )

            response = requests.get(
                url,
                timeout=20
            )

            data = response.json()

            matches = data.get("data", [])

            print(f"LIVE матчей: {len(matches)}")

            for match in matches:

                try:

                    # ===================
                    # LIVE СТАТУС
                    # ===================

                    status = str(
                        match.get("status_name", "")
                    ).lower()

                    if "live" not in status:
                        continue

                    # ===================
                    # МИНУТА
                    # ===================

                    minute = int(
                        match.get("timer", {})
                        .get("tm", 0)
                    )

                    # Только 18-35
                    if minute < 18 or minute > 35:
                        continue

                    # ===================
                    # ЛИГА
                    # ===================

                    league = str(
                        match.get("league_name", "")
                    )

                    allowed = False

                    for top in TOP_LEAGUES:

                        if top.lower() in league.lower():

                            allowed = True

                    if not allowed:
                        continue

                    # ===================
                    # КОМАНДЫ
                    # ===================

                    home = match.get(
                        "home_team",
                        "Home"
                    )

                    away = match.get(
                        "away_team",
                        "Away"
                    )

                    # ===================
                    # СЧЕТ
                    # ===================

                    home_score = int(
                        match.get("score_home", 0)
                    )

                    away_score = int(
                        match.get("score_away", 0)
                    )

                    # Максимум 1 гол
                    if home_score + away_score > 1:
                        continue

                    # ===================
                    # ID
                    # ===================

                    match_id = str(
                        match.get("id")
                    )

                    if match_id in sent_matches:
                        continue

                    sent_matches.add(match_id)

                    # ===================
                    # СИГНАЛ
                    # ===================

                    text = (
                        f"⚽ Football Goal AI\n\n"
                        f"🔥 LIVE сигнал на гол\n\n"
                        f"🏆 {league}\n\n"
                        f"⚔️ {home} vs {away}\n\n"
                        f"📊 Счет:\n"
                        f"{home_score} - {away_score}\n\n"
                        f"⏱ Минута:\n"
                        f"{minute}\n\n"
                        f"📡 Реальный LIVE матч\n"
                        f"🔥 Высокий темп игры"
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

        # Проверка каждую минуту
        await asyncio.sleep(60)

# ====================================
# КОМАНДЫ
# ====================================

@dp.message(Command("start"))
async def start_cmd(message: types.Message):

    text = (
        "⚽ Football Goal AI\n\n"
        "🔥 LIVE сигналы на гол\n"
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

@dp.message(Command("status"))
async def status_cmd(message: types.Message):

    await message.answer(
        "✅ Бот активен\n"
        "📡 LIVE сканирование включено"
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
        "🔥 Поиск голов в 1 тайме"
    )

# ====================================
# СТАРТ БОТА
# ====================================

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
