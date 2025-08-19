import re
import requests
import json
from telegram import Update
from telegram.ext import ContextTypes
from states import CREATE_PRODUCT, MAIN_MENU
from config import URL
from handlers.qrHandler import is_valid_product_code

async def create_product_entry_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(
        "📦 *Add a New Product*\n\n"
        "Please enter the product details *line by line* in the following order:\n\n"
        "<b>Format:</b>\n"
        "<pre>"
        "1. PRODUCTNAME   → Name of the product\n"
        "2. FORMULATION   → Form type (e.g., Tablets, Syrup)\n"
        "3. QUANTITY      → Number of units\n"
        "4. BRAND         → Brand name\n"
        "5. STRENGTH      → Strength or dosage (e.g., 40mg)\n"
        "6. PACKSIZE      → Packaging info (e.g., 7 tablet strips)\n"
        "7. EXPIRY        → Expiry date (YYYY-MM-DD)\n"
        "</pre>\n\n"
        "<b>Example:</b>\n"
        "<pre>"
        "Test\n"
        "Tablets\n"
        "32\n"
        "Vencid\n"
        "40mg\n"
        "7 tablet strips\n"
        "2026-07-30\n"
        "</pre>\n\n"
        "⚠️ Please follow the order exactly and stick to the formats shown."
    )

    return CREATE_PRODUCT

async def create_product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    number_pattern = r"^\d+$"
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    lines = update.message.text.strip().split("\n")

    # If format is wrong
    if len(lines) != 7 or not re.match(number_pattern, lines[2]) or not re.match(date_pattern, lines[6]):
        await update.message.reply_html(
            "❌ Error! Please follow the <b>exact order</b> and use the correct formats below:\n\n"
            "<b>Format:</b>\n"
            "<pre>"
            "1. PRODUCTNAME   → Name of the product\n"
            "2. FORMULATION   → Form type (e.g., Tablets, Syrup)\n"
            "3. QUANTITY      → Number of units\n"
            "4. BRAND         → Brand name\n"
            "5. STRENGTH      → Strength or dosage (e.g., 40mg)\n"
            "6. PACKSIZE      → Packaging info (e.g., 7 tablet strips)\n"
            "7. EXPIRY        → Expiry date (YYYY-MM-DD)\n"
            "</pre>\n\n"
            "<b>Correct Example:</b>\n"
            "<pre>"
            "Test\n"
            "Tablets\n"
            "32\n"
            "Vencid\n"
            "40mg\n"
            "7 tablet strips\n"
            "2026-07-30\n"
            "</pre>"
        )
        return CREATE_PRODUCT

    new_product = {
        "PRODUCTNAME": lines[0],
        "FORMULATION": lines[1],
        "QUANTITY": lines[2],
        "BRAND": lines[3],
        "STRENGTH": lines[4],
        "PACKSIZE": lines[5],
        "EXPIRY": lines[6]
    }

    payload = {
        "method": "POST",
        "new_product": json.dumps(new_product)
    }

    response = requests.post(URL, data=payload)
    response = response.json() # Convert to JSON

    if response["code"] != 200:
        await update.message.reply_text(
            f"❌ Operation Failed\n\n"
            f"📝 Message: {response.get('message', 'Unknown error')}\n"
            f"🔢 Code: {response.get('code', '-')}\n"
            f"✅ Success: {response.get('success', False)}"
        )

    else:
        await update.message.reply_text(
            f"📦 Item Successfully Created:\n"
            f"PRODUCTNAME: {lines[0]}\n"
            f"FORMULATION: {lines[1]}\n"
            f"QUANTITY: {lines[2]}\n"
            f"BRAND: {lines[3]}\n"
            f"STRENGTH: {lines[4]}\n"
            f"PACKSIZE: {lines[5]}\n"
            f"EXPIRY: {lines[6]}\n"
            f'ITEM_CODE: {response["new_item_code"]}\n'
        )
    await update.message.reply_text(
        "You're in Create mode. Type /cancel anytime to exit."
    )
    return CREATE_PRODUCT
