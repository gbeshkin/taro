import os
import random
import telebot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "Puudub TELEGRAM_BOT_TOKEN keskkonnamuutuja. "
        "Lisa see Railway seadetes (Variables)."
    )

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

TAROT_ADVICES = [
    {
        "name": "Narr",
        "emoji": "🃏",
        "text": "Uus algus on sinu ees. Luba endal katsetada ja ära karda näida algajana."
    },
    {
        "name": "Maag",
        "emoji": "🪄",
        "text": "Sul on juba kõik vajalikud vahendid. Kasuta oma oskusi enesekindlamalt."
    },
    {
        "name": "Ülempreestrinna",
        "emoji": "🌙",
        "text": "Kuula oma sisetunnet. Kõik vastused ei tule loogika, vaid vaikuse kaudu."
    },
    {
        "name": "Keisrinna",
        "emoji": "🌿",
        "text": "Hoolitse enda eest. Kui sina oled täis, saad ka teisi toetada."
    },
    {
        "name": "Keiser",
        "emoji": "🛡️",
        "text": "Võta vastutus ja sea selged piirid. Struktuur aitab sul edasi liikuda."
    },
    {
        "name": "Armastajad",
        "emoji": "💞",
        "text": "Valik, mida teed südamest, toetab sind pikemas plaanis kõige rohkem."
    },
    {
        "name": "Kaarik",
        "emoji": "🏇",
        "text": "Liigu edasi, isegi kui kõik pole ideaalne. Tempo loob võimalusi."
    },
    {
        "name": "Õiglus",
        "emoji": "⚖️",
        "text": "Ole enda ja teistega aus. Tasakaal saabub, kui oled õiglane."
    },
    {
        "name": "Mõõdukuse kaart",
        "emoji": "💧",
        "text": "Ära torma. Väikesed järjepidevad sammud on praegu parem kui suured hüpped."
    },
    {
        "name": "Täht",
        "emoji": "⭐",
        "text": "Ära kaota lootust. Isegi kui praegu on hämar, on suunas valgustamas selge eesmärk."
    },
]

START_TEXT = (
    "Tere! 👋\n\n"
    "See bot annab sulle väikese <b>„Nõuanne Taro kaartidelt“</b> stiilis sõnumi.\n\n"
    "➤ Kirjuta mulle lihtsalt oma küsimus või olukord.\n"
    "Ma loosin sulle sümboolse kaardi ja jagan lühikest nõuannet.\n\n"
    "<i>See ei ole ennustus ega professionaalne nõustamine, vaid väike peegeldus ja inspiratsioon.</i> 🔮"
)

HELP_TEXT = (
    "Kuidas bot töötab?\n\n"
    "1️⃣ Kirjuta oma küsimus või olukord (nt „Töömuutus“, „Suhe“, „Millele keskenduda sel kuul?“).\n"
    "2️⃣ Bot loosib ühe Taro-kaardi sümboli ja annab lühikese nõuande.\n"
    "3️⃣ Soovi korral saad kohe uue küsimuse kirjutada.\n\n"
    "Võid küsida ükskõik mida – oluline on, et sõnum aitaks sul teemat teise nurga alt vaadata. 🙂"
)


def pick_tarot_advice() -> dict:
    return random.choice(TAROT_ADVICES)


@bot.message_handler(commands=["start"])
def handle_start(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        START_TEXT,
    )


@bot.message_handler(commands=["help"])
def handle_help(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        HELP_TEXT,
    )


@bot.message_handler(func=lambda msg: True, content_types=["text"])
def handle_question(message: telebot.types.Message):
    user_text = (message.text or "").strip()

    card = pick_tarot_advice()

    reply_parts = [
        f"{card['emoji']} <b>{card['name']}</b>",
        "",
        f"🔮 Nõuanne: {card['text']}",
    ]

    if user_text:
        reply_parts.extend([
            "",
            f"💭 Sinu küsimus: <i>{user_text}</i>",
        ])

    reply_parts.append("")
    reply_parts.append("Soovi korral kirjuta uus küsimus ja loosime järgmise kaardi. 🎴")

    reply_text = "\n".join(reply_parts)

    bot.send_message(
        message.chat.id,
        reply_text,
    )


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
