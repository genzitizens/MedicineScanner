from telegram import Update
from telegram.ext import ContextTypes

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I didn't understand that. Please use /start to start or read through the commands using /help or use /cancel to exit.")