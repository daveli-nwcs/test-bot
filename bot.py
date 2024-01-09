import os

import telebot
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

current_users = []


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "How can i help you?")

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Check-in', callback_data='check-in'
        )
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Check-out', callback_data='check-out'
        )
    )
    
@bot.message_handler(commands=['status'])
def status_command(message):
    print_queue(message)


@bot.message_handler(commands=['info'])
def info_command(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Define a message handler
@bot.message_handler(func=lambda msg: True)
def callback(message):
    data = message.text
    if data.startswith('check-in-'):
        check_in_queue(message.id , message.from_user.username)
    if data.startswith('check-out-'):
        check_out_queue(message.id, message.from_user.username)
        
    # bot.reply_to(message, message.text)

def check_in_queue(id, username):
    if username not in current_users:
        current_users.append(username)
        bot.answer_callback_query(id, text="You are checked-in successfully")
    else:
        bot.answer_callback_query(id, text="You are already checked-in")

def check_out_queue(id, username):
    if username in current_users:
        current_users.remove(username)
        bot.answer_callback_query(id, text="You are checked-out successfully")
    else:
        bot.answer_callback_query(id, text="You are not in the queue")
        
def print_queue(message):
    result = "Current queue: "
    for index, item in enumerate(current_users):
        result += "\n" + str(index + 1) + ": " + item
    result += "\n Total: " + str(len(current_users))
    bot.reply_to(message, result)


# Start the bot
bot.polling()

