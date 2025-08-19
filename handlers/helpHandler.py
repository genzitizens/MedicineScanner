from telegram import Update
from telegram.ext import ContextTypes

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the command /help is issued."""
    await update.message.reply_text(
        "🤖 *Welcome to the DnG Database Bot!*\n\n"
        "This bot helps field teams manage inventory quickly and accurately.\n\n"

        "*📌 Main Commands:*\n"
        "• `/add_inventory` – Add stock of an existing product\n"
        "• `/deduct_inventory` – Deduct stock of an existing product\n"
        "• `/create_product` – Register a new product in the database\n"
        "• `/generate_qr` – Generate a QR code for a product\n\n"

        "*⚙️ How it works:*\n"
        "1. Use `/add_inventory` or `/deduct_inventory`\n"
        "   • Send a photo of the product’s QR code *or* type the product code manually\n"
        "   • Enter the quantity and remarks (e.g. `10,Restocked shelf A`)\n"
        "   • The database will be updated and logged automatically ✅\n\n"

        "2. Use `/create_product`\n"
        "   • Enter the product details *line by line* in the following order:\n\n"
        "     1. Product Name\n"
        "     2. Formulation (e.g., Tablets, Syrup)\n"
        "     3. Quantity (number of units)\n"
        "     4. Brand Name\n"
        "     5. Strength/Dosage (e.g., 40mg)\n"
        "     6. Pack Size (e.g., 7 tablet strips)\n"
        "     7. Expiry Date (YYYY-MM-DD)\n\n"
        "   *Example:*\n"
        "   Paracetamol\n"
        "   Tablets\n"
        "   32\n"
        "   Paracetamol\n"
        "   40mg\n"
        "   7 tablet strips\n"
        "   2026-07-30\n\n"
        "   ⚠️ Please follow the order exactly and stick to the formats shown.\n\n"

        "3. Use `/generate_qr`\n"
        "   • Enter a valid product code (DnG convention)\n"
        "   • The bot will return a QR code image you can paste onto the product\n",

        parse_mode="Markdown"
    )