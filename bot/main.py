import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Load .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")


# --- Command Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome here!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How can I help you today?')


# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Welcome here! I am Jiivorn bot. You can ask me like hello, how are you, what is your name.')
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome here! I am Jiivorn bot. You can ask me like:\n'
        '🥳 hello\n'
        '🥳 how are you\n'
        '🥳 what is your name'
    )

# --- Response Logic ---
def handle_response(text: str) -> str:
    processed = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return "I’m good! How about you?"
    if 'what is your name' in processed:
        return "I am Jiivorn bot."
    return "I don't understand what you wrote."


# --- Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
            await update.message.reply_text(response)
    else:
        response = handle_response(text)
        print("Bot:", response)
        await update.message.reply_text(response)


# --- Error Handler ---
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# --- Main ---
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log errors
    app.add_error_handler(error)

    print('Bot is polling...')
    app.run_polling(poll_interval=3)
