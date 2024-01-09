import os

import telebot


bot = telebot.TeleBot("6963305401:AAHlMPzZ_bDVB0lO_6YpUoj6p9eQnJn3jQEso")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, “This is a simple Telegram bot implemented in Python.”)

# Define a message handler
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)



# Start the bot
bot.polling()

