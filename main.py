#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from io import BytesIO

import re
from typing import Any, Union, Coroutine

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

from config import TOKEN
from handlers.deductInventoryHandler import deduct_inventory_handler, deduct_inventory_entry_handler
from handlers.qrHandler import generate_qr_handler, handleProductCode
from handlers.unknownHandler import handle_unknown
from states import MAIN_MENU, WAITING_FOR_PRODUCT_CODE, CREATE_PRODUCT, ADD_INVENTORY, DEDUCT_INVENTORY
from handlers.startHandler import handle_start
from handlers.cancelHandler import handle_cancel
from handlers.helpHandler import handle_help
from handlers.createProductHandler import create_product_entry_handler, create_product_handler
from handlers.addInventoryHandler import add_inventory_entry_handler, add_inventory_handler

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).read_timeout(60).write_timeout(60).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handle_start),
                      CommandHandler("cancel", handle_cancel),
                      CommandHandler("help", handle_help),  # existing cancel handler
                      MessageHandler(filters.TEXT | filters.COMMAND, handle_unknown)],# catch-all for unknown text
        states = {
            MAIN_MENU: [
            CommandHandler("start", handle_start),
            CommandHandler("add_inventory", add_inventory_entry_handler),
            CommandHandler("deduct_inventory", deduct_inventory_entry_handler),
            CommandHandler("generate_qr", generate_qr_handler),
            CommandHandler("create_product",create_product_entry_handler),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown) ], # fallback for bad input]

            WAITING_FOR_PRODUCT_CODE : [
                CommandHandler("start", handle_start),
                CommandHandler("cancel", handle_cancel),
                CommandHandler("help", handle_help),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handleProductCode)
            ],

            CREATE_PRODUCT:[
                CommandHandler("start", handle_start),
                CommandHandler("cancel", handle_cancel),
                CommandHandler("help", handle_help),
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_product_handler)
            ],

            ADD_INVENTORY: [
                CommandHandler("start", handle_start),
                CommandHandler("cancel", handle_cancel),
                CommandHandler("help", handle_help),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_inventory_handler),
                MessageHandler(filters.PHOTO, add_inventory_handler),
            ],

            DEDUCT_INVENTORY :[
                CommandHandler("start", handle_start),
                CommandHandler("cancel", handle_cancel),
                CommandHandler("help", handle_help),
                MessageHandler(filters.TEXT & ~filters.COMMAND, deduct_inventory_handler),
                MessageHandler(filters.PHOTO, deduct_inventory_handler),
            ],
        },
        fallbacks=[
            CommandHandler("start", handle_start),
            CommandHandler("cancel", handle_cancel),
            CommandHandler("help",handle_help),# existing cancel handler
            MessageHandler(filters.ALL, handle_unknown),  # catch-all fallback
            #MessageHandler(filters.TEXT |~filters.COMMAND, handle_unknown)# catch-all for unknown text
        ],
    )

    # on non command i.e message - echo the message on Telegram
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()