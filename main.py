import telebot
import logging  # Just debugger that will be cut after deploy
from config import API_TOKEN
from models.database import db, Roommate
import utils.utils as u

logger = telebot.logger  # Just debugger that will be cut after deploy
telebot.logger.setLevel(logging.DEBUG)  # Just debugger that will be cut after deploy

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, "Welcome to our flat!")


@bot.message_handler(commands=['help'])
def help_command_handler(message):
    bot.send_message(message.chat.id, "As you can see we have only one rule - no guests!")


@bot.message_handler(commands=['roommate'])
def roommate_command_handler(message):
    telegram_id = message.user.id

    if u.database_unique_user(bot, message, telegram_id, Roommate):
        username = message.user.first_name + " " + message.user.last_name
        Roommate.insert_one({"Name": username,
                             "Telegram_id": telegram_id,
                             "Deposit": 0
                             })
    else:
        bot.send_message(message.chat.id, "You are already a roommate.")


@bot.message_handler(commands=['insert'])
def insert_command_handler(message):
    message_content = message.text
    arg = u.extract_arg(message_content, bot, message)
    if arg is not None:
        if u.pull_into_database(arg, bot, message):
            bot.reply_to(message, "Ok, we got your transfer of " + str(arg))
        else:
            bot.send_message(message.chat.id, "Something went wrong... Try again later")


@bot.message_handler(func=lambda m: True)
def text_message_handler(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        pass
    else:
        bot.send_message(message.chat.id, "You better use commands, I can't understand you anyway...")


bot.polling()
