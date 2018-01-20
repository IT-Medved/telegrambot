import telebot
import os
from flask import Flask, request
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
api_token = os.environ['api_token']
bot = telebot.TeleBot(api_token)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    logging.debug("echo_message")
    bot.reply_to(message, message.text)

@server.route("/bot" + api_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    logging.debug("getMessage")
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://testplafrorm.herokuapp.com/bot" + api_token)
    return "!", 200

webhook()
server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
server = Flask(__name__)
