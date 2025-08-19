from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from states import MAIN_MENU

import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [["/add_inventory", "/deduct_inventory", "/generate_qr", "/create_product"]]
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)
    await update.message.reply_html(
        f"👋 Hi! I'm the DnG Database Bot. Here’s what I can help you with:\n\n"
        f"• 📦 Add inventory -> /add_inventory\n"
        f"• ➖ Deduct inventory -> /deduct_inventory\n"
        f"• 🔖 Generate QR codes -> /generate_qr\n"
        f"• 🆕 Create new products -> /create_product\n\n"
        f"Type /help anytime for more details.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Choose an action",
            resize_keyboard=True
        ),
    )
    return MAIN_MENU