from datetime import datetime

import numpy as np
import cv2
import json

import requests
from telegram import Update
from telegram.ext import ContextTypes

from handlers.qrHandler import is_valid_product_code
from states import ADD_INVENTORY

from config import URL

async def add_inventory_entry_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(
        "<b>📦 Add Inventory</b>\n\n"
        "Please either:\n"
        "1. Take a picture of the QR code of the item\n"
        "2. Or send the item code directly\n\n"
        "➡️ Make sure the QR code or code is clear to avoid errors."
    )
    return ADD_INVENTORY
'''
async def add_inventory_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:  # ✅ handle photo
        await update.message.reply_text("Image detected. Decoding QR code...")
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        result = decode_qr_opencv(photo_bytes)
        if result:
            await update.message.reply_text(f"✅ Code `{result}` accepted.", parse_mode="Markdown")

        else:
            await update.message.reply_text("⚠️ Could not detect any QR code. Please try again.")
            

    elif update.message.text:  # ✅ handle text
        if not (is_valid_product_code(update.message.text)):
            await update.message.reply_text(
                "❌ Invalid product code. Please use the format M00001a (starts with M, 5 digits, 1 letter)."
            )
            return ADD_INVENTORY
        await update.message.reply_text(
            f"✅ Code `{update.message.text}` accepted.", parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("❌ Unsupported input. Please send text or a QR code photo.")

    return ADD_INVENTORY
'''
async def add_inventory_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ✅ Case 1: Handle photo (QR code)
    if update.message.photo and "CODE" not in context.user_data:
        await update.message.reply_text("Image detected. Decoding QR code...")
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        result = decode_qr_opencv(photo_bytes)

        if result:
            context.user_data["CODE"] = result
            context.user_data["DATE_TIME"] = datetime.now().isoformat()

            await update.message.reply_text(
                f"✅ Code {result} detected.\n"
                f"👉 Please enter the quantity and remarks in the format:\n"
                f"<quantity>,<remarks>\n\n"
                f"Example: 10,Restocked shelf A\n"
                f"You are in add_inventory mode. Enter /cancel to exit"
            )
            return ADD_INVENTORY
        else:
            await update.message.reply_text("⚠️ Could not detect any QR code. Please try again.")
            return ADD_INVENTORY

    # ✅ Case 2: Handle manual product code text
    elif update.message.text and "CODE" not in context.user_data:
        code = update.message.text.strip()
        if not is_valid_product_code(code):
            await update.message.reply_text(
                "❌ Invalid product code. Please use the format M00001a (starts with M, 5 digits, 1 letter).\n"
                f"You are in add_inventory mode. Enter /cancel to exit\n"
            )
            return ADD_INVENTORY

        context.user_data["CODE"] = code
        context.user_data["DATE_TIME"] = datetime.now().isoformat()

        await update.message.reply_text(
            f"✅ Code {code} detected.\n"
            f"👉 Please enter the quantity and remarks in the format:\n"
            f"<quantity>,<remarks>\n\n"
            f"Example: 10,Restocked shelf A\n"
            f"You are in add_inventory mode. Enter /cancel to exit"
        )
        return ADD_INVENTORY

    # ✅ Case 3: Handle quantity + remarks input
    elif update.message.text and "CODE" in context.user_data:
        try:
            qty_str, remarks = update.message.text.split(",", 1)
            quantity = int(qty_str.strip())
            remarks = remarks.strip()
        except Exception:
            await update.message.reply_text(
                "❌ Invalid format. Please use `<quantity>,<remarks>` (e.g. `5,Restocked shelf A`).\n"
                f"You are in add_inventory mode. Enter /cancel to exit\n"
            )
            return ADD_INVENTORY

        update_data = {
            "CODE": context.user_data["CODE"],
            "OPERATION_TYPE": "ADD",
            "OPERATION_QUANTITY": quantity,
            "REMARKS": remarks,
            "DATE_TIME": context.user_data["DATE_TIME"],
        }

        payload = {
            "method": "PATCH",
            "update": json.dumps(update_data)
        }

        try:
            response = requests.post(URL, data=payload).json()
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to contact server: {e}")
            return ADD_INVENTORY

        if response["code"] != 200:
            await update.message.reply_text(
                f"❌ Operation Failed\n\n"
                f"📝 Message: {response['message']}\n"
                f"You are in add_inventory mode. Enter /cancel to exit\n"
            )
        else:
            await update.message.reply_text(
                f"✅ Operation Successful!\n\n"
                f"📝 Status: {response['message']}\n"
                f"📦 Product: {response['productName']} ({response['productCode']})\n"
                f"🔢 Quantity: {response['previousQuantity']} ➝ {response['updatedQuantity']}\n"
                f"💬 Remarks: {response.get('remarks', '-')}\n"
                f"You are in add_inventory mode. Enter /cancel to exit\n")

        # clear memory for next operation
        context.user_data.clear()
        return ADD_INVENTORY

    # ❌ Unsupported input
    else:
        await update.message.reply_text("❌ Unsupported input. Please send a QR code photo or a product code.\n"
                                        f"You are in add_inventory mode. Enter /cancel to exit\n")
        return ADD_INVENTORY

def decode_qr_opencv(image_bytes):
    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # Try preprocessing the image first
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray)
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(denoised)
    if retval:
        for i, info in enumerate(decoded_info):
            if info:  # Check if decoding was successful
                print(f"QR Code {i}: {info}")
                info_z = info
            else:
                print(f"QR Code {i}: Failed to decode")
    else:
        print("No QR codes detected")

    if points is not None and decoded_info is not None:
        return decoded_info[0]
    return None
