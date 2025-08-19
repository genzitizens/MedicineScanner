import re
from io import BytesIO

import qrcode
from telegram import Update
from telegram.ext import ContextTypes

from states import MAIN_MENU,WAITING_FOR_PRODUCT_CODE

def is_valid_product_code(code: str) -> bool:
    # Example: DnG format like M00001a (starts with 'M', 5 digits, ends with a lowercase letter)
    return re.match(r"^M\d{5}[a-z]$", code) is not None

async def handleProductCode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text.strip()
    if not (is_valid_product_code(code)):
        await update.message.reply_text(
            "❌ Invalid product code. Please use the format M00001a (starts with M, 5 digits, 1 letter)."
        )
        return WAITING_FOR_PRODUCT_CODE
    await update.message.reply_text(
        f"✅ Code `{code}` accepted. Generating QR code...", parse_mode="Markdown"
    )
    img = qrcode.make(code)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # 5. Send the QR image
    await update.message.reply_photo(photo=buffer, caption=f"QR code for: {code}")
    await update.message.reply_text(
        "You're in QR mode. Type /cancel anytime to exit."
    )
    return WAITING_FOR_PRODUCT_CODE


async def generate_qr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(
        rf"🔍 Please input the product code in DnG format (e.g., M00001a) to generate a QR code."
    )
    return WAITING_FOR_PRODUCT_CODE