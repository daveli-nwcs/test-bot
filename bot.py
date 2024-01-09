import os

import telebot
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

current_users = []


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "How can i help you?")

@bot.message_handler(commands=['status'])
def status_command(message):
    print_queue(message)

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
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Check status', callback_data='status'
        )
    )
    bot.send_message(message.chat.id, 'Click for your action', reply_markup=keyboard)




@bot.message_handler(commands=['info'])
def info_command(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Define a message handler
@bot.callback_query_handler(func=lambda call: True)
def callback(message):
    data = message.data
    bot.answer_callback_query(message.id)
    if data.startswith('check-in-'):
        check_in_queue(message)
    if data.startswith('check-out-'):
        check_out_queue(message)
    if data.startswith('status'):
        print_queue(message)
    # bot.reply_to(message, message.text)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.reply_to(message, message.text)
    
def check_in_queue(message):
    username = message.from_user.username
    chat_id = message.chat.id
    if username not in current_users:
        bot.send_chat_action(chat_id, 'typing')
        current_users.append(username)
        bot.send_message(chat_id, "You are checked-in successfully")
    else:
        bot.send_message(chat_id, "You are already checked-in")

def check_out_queue(message):
    username = message.from_user.username
    chat_id = message.chat.id
    if username in current_users:
        current_users.remove(username)
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(chat_id, "You are checked-out successfully")
    else:
        bot.send_message(chat_id, "You are not in the queue")
        
def print_queue(message):
    chat_id = message.chat.id
    result = "Current queue: "
    for index, item in enumerate(current_users):
        result += "\n" + str(index + 1) + ": " + item
    result += "\n Total: " + str(len(current_users))
    bot.send_message(chat_id, result)


# Start the bot
bot.polling()

