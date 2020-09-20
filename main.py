import telebot
import logging  # Just debugger that will be cut after deploy
from config import API_TOKEN
from models.database import Roommate
import utils.utils as u
import utils.db_ulils as db_u

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
    telegram_id = message.from_user.id

    if db_u.database_unique_user(bot, message, telegram_id):
        username = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
        Roommate.insert_one({"Name": str(username),
                             "Telegram_id": int(telegram_id),
                             "Deposit": int(0)
                             })
        bot.send_message(message.chat.id, "Successfully added to database.")
    else:
        bot.send_message(message.chat.id, "You are already a roommate.")


@bot.message_handler(commands=['insert'])
def insert_command_handler(message):
    if db_u.in_database_checker(bot, message, message.from_user.id):
        message_content = message.text
        arg = u.extract_arg(message_content, bot, message)
        if arg is not None:
            db_u.pull_into_database(arg, bot, message, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "You're not a roommate, to became a roommate - send /roommate...")


@bot.message_handler(commands=['balance'])
def balance_display(message):
    db_u.balance_counter(bot, message)


@bot.message_handler(commands=['details'])
def balance_detail_display(message):
    pass


@bot.message_handler(func=lambda m: True)
def text_message_handler(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        pass
    else:
        bot.send_message(message.chat.id, "You better use commands, I can't understand you anyway...")


bot.polling()
