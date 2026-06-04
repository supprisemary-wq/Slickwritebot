import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Turn on logging to monitor the bot
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# KEEP THE QUOTES EXACTLY LIKE THIS
TOKEN = "8941435878:AAFFpIeeMyLhJrmN_TiOSCNKwE8TgHOIuVs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 Hello! Your brand new SlickWriteBot is officially working live!")

async def check_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_chat_action(action="typing")
    
    api_url = "https://api.languagetool.org/v2/check"
    try:
        response = requests.post(api_url, data={'text': user_text, 'language': 'en-US'}).json()
        matches = response.get("matches", [])
        if not matches:
            await update.message.reply_text("✨ No errors found!")
            return
        
        reply = "📝 Suggestions:\n\n"
        for i, match in enumerate(matches[:3], start=1):
            reply += f"❌ Issue {i}: {match.get('message')}\n\n"
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"API Error: {e}")
        await update.message.reply_text("❌ Grammar service is temporarily busy.")

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_grammar))
    
    print("✅ Bot is successfully running...")
    application.run_polling(drop_pending_updates=True)
