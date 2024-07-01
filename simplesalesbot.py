from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN: Final = 'yourtoken'
BOT_USERNAME: Final = '@yourbottag'

catalogs = {
    "1": ["Item 1", "Item 2", "Item 3"],
    "2": ["Item 4", "Item 5", "Item 6"],
    "3": ["Item 7", "Item 8", "Item 9"],
    "4": ["Item 10", "Item 11", "Item 12"],
    "5": ["Item 13", "Item 14", "Item 15"]
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! This is a bot of ... store. Use menu and commands to look at the catalogue of items")

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{catalog}", callback_data=catalog) for catalog in catalogs.keys()]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a catalog:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_catalog = query.data
    items = catalogs.get(selected_catalog, [])
    
    if items:
        keyboard = [
            [InlineKeyboardButton(item, callback_data=f"item_{item}") for item in items]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"You chosen a catalogue {selected_catalog}. Choose item:", reply_markup=reply_markup)

async def item_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item = query.data.split('_')[1]
    
    whatsapp_link = f"https://wa.me/numberhere?text=Give%20me%20{item}"
    await query.edit_message_text(f"You chosen an item: {item}. To purchase, follow the [link]({whatsapp_link}).", parse_mode="Markdown")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("catalog", catalog_command))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(1|2|3|4|5)$"))
    application.add_handler(CallbackQueryHandler(item_handler, pattern="^item_"))

    application.run_polling()

if __name__ == '__main__':
    main()