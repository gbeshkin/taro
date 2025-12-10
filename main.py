import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

TAROT_CARDS = [
    {
        "name": "0. Шут",
        "upright": "Начало, лёгкость, доверие миру, спонтанность.",
        "reversed": "Безответственность, хаос, страх сделать шаг.",
        "advice": "Разреши себе попробовать что-то новое, но не действуй вслепую."
    },
    {
        "name": "I. Маг",
        "upright": "Сила воли, концентрация, ресурсы в твоих руках.",
        "reversed": "Самообман, манипуляции, распыление энергии.",
        "advice": "Соберись и используй то, что у тебя уже есть."
    },
    {
        "name": "II. Верховная Жрица",
        "upright": "Интуиция, внутреннее знание, тишина.",
        "reversed": "Игнорирование интуиции, путаница.",
        "advice": "Замедлись и прислушайся к себе."
    },
]

def get_tarot_message() -> str:
    card = random.choice(TAROT_CARDS)
    reversed_card = random.choice([True, False])

    position = "перевёрнутая" if reversed_card else "прямая"
    meaning = card["reversed"] if reversed_card else card["upright"]

    return (
        "🎴 Твоя подсказка от Таро\n\n"
        f"*{card['name']}* ({position})\n\n"
        f"🔍 Значение: {meaning}\n\n"
        f"💡 Совет: {card['advice']}\n\n"
        "⚠️ Это не предсказание судьбы, а повод задуматься."
    )

def keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎴 Получить подсказку", callback_data="get_hint")]
        ]
    )

async def start_cmd(message: Message):
    await message.answer(
        "Привет 👋\n\n"
        "Я бот «Подсказка от Таро».\n"
        "Нажми кнопку ниже, чтобы вытянуть карту и получить совет.\n\n"
        "Это не гадание, а мягкий символический взгляд на ситуацию 😉",
        reply_markup=keyboard()
    )

async def callback_handler(callback: CallbackQuery):
    if callback.data == "get_hint":
        await callback.message.answer(
            get_tarot_message(),
            parse_mode="Markdown",
            reply_markup=keyboard()
        )
        await callback.answer()

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN в Railway → Variables")

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_cmd, Command("start"))
    dp.callback_query.register(callback_handler, F.data == "get_hint")

    print("✅ Tarot bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
