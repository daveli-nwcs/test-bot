import os
import logging

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

@bot.message_handler(commands=['check-in'])
def checkin_command(message):
    check_in_queue(message, message.from_user)
    
@bot.message_handler(commands=['check-out'])
def checkout_command(message):
    check_out_queue(message, message.from_user)

@bot.message_handler(commands=['info'])
def info_command(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Define a message handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    if data.startswith('check-in'):
        check_in_queue(call.message, call.from_user)
    if data.startswith('check-out'):
        check_out_queue(call.message, call.from_user)
    if data.startswith('status'):
        print_queue(call.message)
    # bot.reply_to(message, message.text)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
#     msg = bot.send_message(message.from_user.id,  """\
# How can I help u?
# """, allow_sending_without_reply=True)
    msg = bot.send_message(None,  """\
How can I help u?
""", allow_sending_without_reply=True)
    bot.register_next_step_handler(msg, start_command)
    # bot.reply_to(message, message.text)

def check_in_queue(message, user):
    username = user.username
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing', 3)
    if username not in current_users:
        current_users.append(username)
        print_queue(message)
    else:
        msg = bot.send_message(chat_id, "You are already checked-in")
        bot.register_next_step_handler(msg, start_command)
    bot.answer_callback_query(message.id)

def check_out_queue(message, user):
    username = user.username
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing', 3)
    if username in current_users:
        current_users.remove(username)
        bot.send_message(chat_id, "You are checked-out successfully")
        print_queue(message)
    else:
        msg = bot.send_message(chat_id, "You are not in the queue")
        bot.register_next_step_handler(msg, start_command)
    bot.answer_callback_query(message.id)
    bot.register_next_step_handler(message, start_command)

        
def print_queue(message):
    chat_id = message.chat.id
    result = "Current queue: "
    for index, item in enumerate(current_users):
        result += "\n" + str(index + 1) + ": " + item
    result += "\n Total: " + str(len(current_users))
    msg = bot.send_message(chat_id, result)
    bot.answer_callback_query(message.id)
    bot.register_next_step_handler(msg, start_command)



# Start the bot
bot.infinity_polling()


