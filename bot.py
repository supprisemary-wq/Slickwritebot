import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your correct token with quotation marks
TOKEN = "8941435878:AAFFpIeeMyLhJrmN_TiOSCNKwE8TgHOIuVs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        "Hi! 👋\n\n"
        "I am <b>SlickWriteBot</b>. Send me any text, and I will check it for grammar errors!"
    )

async def check_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_chat_action(action="typing")

    api_url = "https://api.languagetool.org/v2/check"
    data = {'text': user_text, 'language': 'en-US'}
    
    try:
        response = requests.post(api_url, data=data).json()
        matches = response.get("matches", [])
        
        if not matches:
            await update.message.reply_text("✨ Your text looks perfect!")
            return

        reply_message = "📝 <b>Suggestions:</b>\n\n"
        for i, match in enumerate(matches[:3], start=1):
            reply_message += f"<b>{i}. Issue:</b> {match.get('message')}\n\n"
            
        await update.message.reply_html(reply_message)
    except Exception as e:
        await update.message.reply_text("❌ An error occurred.")

if __name__ == "__main__":
    # Modern, clean setup to completely bypass the 'Updater' error bug
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_grammar))
    
    print("✅ Bot is successfully running...")
    application.run_polling(drop_pending_updates=True)
