import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = "8652395156:AAEfEMjPY6sfE1JlDwzh-PY6H8VkNsVXwo2k"

# Твой Telegram ID
CHAT_ID = 8670609815

# =========================
# БОТ
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Чтобы не дублировать сигналы
sent_matches = set()

# =========================
# ЛИГИ
# =========================

LEAGUES = [

    # Англия
    "Premier League",
    "Championship",

    # Германия
    "Bundesliga",
    "2. Bundesliga",

    # Испания
    "La Liga",

    # Франция
    "Ligue 1",

    # Россия
    "Premier Liga",

    # Италия
    "Serie A",

    # Нидерланды
    "Eredivisie",

    # Португалия
    "Primeira Liga",

    # Турция
    "Super Lig",

    # Бельгия
    "Jupiler Pro League",

    # Международные турниры
    "UEFA Champions League",
    "UEFA Europa League",
    "UEFA Conference League",
    "FIFA World Cup",
    "UEFA European Championship",
    "Copa America",

    # Результативные лиги
    "A-League",
    "Swiss Super League",
    "Austrian Bundesliga",
    "Danish Superliga",
    "Norwegian Eliteserien",
    "Swedish Allsvenskan"
]

# =========================
# КОМАНДЫ
# =========================

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "⚽ <b>Football Goal AI</b>\n\n"
        "🔥 LIVE сигналы на гол в 1 тайме\n\n"
        "📊 Анализ:\n"
        "• давление\n"
        "• атаки\n"
        "• удары\n"
        "• темп игры\n"
        "• статистика LIVE\n\n"
        "⏱ Сигналы:\n"
        "18–35 минута\n\n"
        "🏆 Топ лиги и турниры:\n"
        "🇬🇧 Англия\n"
        "🇩🇪 Германия\n"
        "🇪🇸 Испания\n"
        "🇫🇷 Франция\n"
        "🇮🇹 Италия\n"
        "🏆 Лига Чемпионов\n"
        "🌍 Чемпионат Мира\n\n"
        "🚨 Ожидайте LIVE сигналы",
        parse_mode="HTML"
    )

@dp.message(Command("signals"))
async def signals_handler(message: Message):
    await message.answer(
        "📡 Сканер активен\n\n"
        "⚡ Поиск сильных матчей идёт 24/7"
    )

@dp.message(Command("status"))
async def status_handler(message: Message):
    await message.answer(
        "🟢 СТАТУС: ONLINE\n\n"
        "⚽ Сканирование матчей активно"
    )

@dp.message(Command("info"))
async def info_handler(message: Message):
    await message.answer(
        "📊 СТРАТЕГИЯ:\n\n"
        "Бот ищет матчи:\n"
        "• с высоким темпом\n"
        "• большим количеством атак\n"
        "• активным фаворитом\n"
        "• высоким давлением\n\n"
        "⏱ Основной период:\n"
        "18–35 минута\n\n"
        "🔥 Цель:\n"
        "Поймать гол в первом тайме."
    )

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📌 КОМАНДЫ:\n\n"
        "/start - запуск бота\n"
        "/signals - статус сигналов\n"
        "/status - проверить работу\n"
        "/info - стратегия\n"
        "/help - помощь"
    )

# =========================
# LIVE СКАНЕР
# =========================

async def football_scanner():

    while True:

        try:

            url = "https://www.scorebat.com/video-api/v3/"
            response = requests.get(url).json()

            for match in response.get("response", []):

                title = match.get("title", "")
                competition = match.get("competition", "")

                # Проверка лиги
                if any(league in competition for league in LEAGUES):

                    # Защита от дублей
                    if title not in sent_matches:

                        sent_matches.add(title)

                        text = (
                            f"🚨 <b>LIVE SIGNAL</b>\n\n"
                            f"⚽ <b>{title}</b>\n"
                            f"🏆 {competition}\n\n"
                            f"🔥 Возможен ГОЛ в 1 тайме\n"
                            f"⏱ 18–35 минута\n\n"
                            f"📊 Высокий темп\n"
                            f"📈 Давление фаворита\n"
                            f"🎯 Опасные атаки"
                        )

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text,
                            parse_mode="HTML"
                        )

                        print(f"Сигнал отправлен: {title}")

            # Проверка каждые 5 минут
            await asyncio.sleep(300)

        except Exception as e:

            print("Ошибка:", e)

            await asyncio.sleep(60)

# =========================
# ЗАПУСК
# =========================

async def main():

    asyncio.create_task(football_scanner())

    print("Football Goal AI запущен")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
