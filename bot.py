import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Turn on extra heavy logging to catch errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# PASTE YOUR TOKEN EXACTLY BETWEEN THE QUOTES BELOW
TOKEN = 8941435878:AAFFpIeeMyLhJrmN_TiOSCNKwE8TgHOIuVs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("--- START COMMAND RECEIVED ---")  # This shows up in Render logs
    await update.message.reply_text("👋 Hello! SlickWriteBot is officially working live!")

async def check_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    print(f"--- CHECKING TEXT: {user_text} ---")
    
    api_url = "https://api.languagetool.org/v2/check"
    try:
        response = requests.post(api_url, data={'text': user_text, 'language': 'en-US'}).json()
        matches = response.get("matches", [])
        if not matches:
            await update.message.reply_text("✨ No errors found!")
            return
        
        reply = "📝 Suggestions:\n"
        for match in matches[:3]:
            reply += f"❌ Issue: {match.get('message')}\n\n"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    print("--- BOT IS LOGGING IN TO TELEGRAM ---")
    
    # Quick security check to make sure you replaced the placeholder text
    if "YOUR_REAL" in TOKEN or TOKEN == "":
        print("❌ ERROR: You forgot to replace the placeholder with your actual BotFather token!")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_grammar))

    print("✅ BOT IS LIVE AND LISTENING! TRY SENDING /start NOW.")
    application.run_polling(drop_pending_updates=True) # Forces Telegram to clear old stuck messages

if __name__ == "__main__":
    main()
