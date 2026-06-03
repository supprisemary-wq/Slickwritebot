import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve the token from environment variables (crucial for Render deployment)
8941435878:AAFFpIeeMyLhJrmN_TiOSCNKwE8TgHOIuVs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        "I am <b>SlickWriteBot</b>, your AI writing assistant. "
        "Send me any text or paragraph, and I will check it for grammar errors, "
        "style improvements, and spelling mistakes!"
    )

async def check_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the user's text for grammar issues using the LanguageTool API."""
    user_text = update.message.text
    
    # Let the user know the bot is working
    await update.message.reply_chat_action(action="typing")

    # Call the free LanguageTool API
    api_url = "https://api.languagetool.org/v2/check"
    data = {
        'text': user_text,
        'language': 'en-US'
    }
    
    try:
        response = requests.post(api_url, data=data).json()
        matches = response.get("matches", [])
        
        if not matches:
            await update.message.reply_text("✨ Your text looks perfect! No errors or style improvements found.")
            return

        # Format the corrections
        reply_message = "📝 <b>Writing Improvements Found:</b>\n\n"
        
        for i, match in enumerate(matches[:5], start=1): # Limit to top 5 suggestions to prevent clutter
            message = match.get("message")
            offset = match.get("offset")
            length = match.get("length")
            wrong_text = user_text[offset:offset+length]
            
            # Extract replacements
            replacements = [rep.get("value") for rep in match.get("replacements", [])[:3]]
            suggestions = ", ".join(replacements) if replacements else "None"
            
            reply_message += f"<b>{i}. Context:</b> \"...{wrong_text}...\"\n"
            reply_message += f"💡 <b>Issue:</b> {message}\n"
            reply_message += f"✅ <b>Suggestions:</b> {suggestions}\n\n"
            
        if len(matches) > 5:
            reply_message += f"<i>...and {len(matches) - 5} more suggestions found.</i>"
            
        await update.message.reply_html(reply_message)

    except Exception as e:
        logger.error(f"Error calling LanguageTool API: {e}")
        await update.message.reply_text("❌ Sorry, I encountered an error while processing your text. Please try again later.")

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        logger.error("No bot token found! Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_grammar))

    # Run the bot using Long Polling (ideal for lightweight setups on Render)
    application.run_polling()

if __name__ == "__main__":
    main()
