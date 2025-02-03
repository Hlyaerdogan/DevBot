import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re

# Bot token
TOKEN = 'YOUR_BOT_TOKEN'

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# List of facts
facts = [
    "Python was created in the 1980s by Guido van Rossum.",
    "JavaScript was originally called Mocha.",
    "The first computer program was written in machine code.",
    "Over 60% of websites today use PHP.",
    "Benjamin Franklin created the first concept of a 'digital' signature."
]

# List of programming tips
tips = [
    "Don't fear mistakes — it's part of the learning process!",
    "Practice is key to success, don't be afraid to make mistakes.",
    "Reading documentation always pays off.",
    "Programming is not just about writing code, it's about solving problems.",
    "Always check your code for errors before running it."
]

# Visit counter
user_visits = {}

# /start command handler
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Hello, {user.first_name}! I'm your programming bot. Use /fact for a random fact, /tip for a tip, and /calc for calculations.")

# /fact command handler
def fact(update, context):
    random_fact = random.choice(facts)
    update.message.reply_text(random_fact)

# /tip command handler
def tip(update, context):
    random_tip = random.choice(tips)
    update.message.reply_text(random_tip)

# /calc command handler
def calc(update, context):
    try:
        expression = ' '.join(context.args)
        result = eval(expression)
        update.message.reply_text(f"Result: {result}")
    except Exception as e:
        update.message.reply_text("Error in calculation. Check the expression.")

# Message handler
def handle_message(update, context):
    user = update.message.from_user
    if user.id not in user_visits:
        user_visits[user.id] = 1
    else:
        user_visits[user.id] += 1

    visit_count = user_visits[user.id]
    update.message.reply_text(f"Welcome, {user.first_name}! This is your {visit_count}-th visit.")

# Error handler
def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Adding command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fact", fact))
    dp.add_handler(CommandHandler("tip", tip))
    dp.add_handler(CommandHandler("calc", calc))

    # Adding message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Error handler
    dp.add_error_handler(error)

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
