import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot_telegram import handle_message

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Fork & Flame! 🔥\n\n"
        "How can I help you today?\n\n"
        "📌 *Book a table* — type 'reserve'\n"
        "🕐 *Our hours* — type 'hours'\n"
        "📍 *Location* — type 'location'\n"
        "🍽️ *Menu* — type 'menu'\n"
        "🥗 *Vegetarian options* — type 'vegetarian'\n"
        "🚗 *Parking* — type 'parking'\n"
        "📶 *WiFi* — type 'wifi'",
        parse_mode="Markdown"
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = str(update.message.from_user.id)
    message = update.message.text.strip().lower()
    response = await handle_message(user_id, message)
    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Fork & Flame Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
