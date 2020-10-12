import telebot
import logging  # Just debugger that will be cut after deploy
import requests, json
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
    message_content = message.text
    password = u.extract_pass(message_content)
    if password is not None:
        if u.password_checker(password):
            bot.delete_message(message.chat.id, message.message_id)
            if db_u.database_unique_user(bot, message, telegram_id):

                if message.from_user.last_name is None:
                    username = str(message.from_user.first_name)
                else:
                    username = str(message.from_user.first_name) + " " + str(message.from_user.last_name)

                Roommate.insert_one({"Name": str(username),
                                     "Telegram_id": int(telegram_id),
                                     "Deposit": int(0)
                                     })
                bot.send_message(message.chat.id, "Successfully added to database.")
            else:
                bot.send_message(message.chat.id, "You are already a roommate.")
        else:
            bot.send_message(message.chat.id, "Access to this command denied...")
    else:
        bot.send_message(message.chat.id, "Correct your input data to /roommate <password> format...")


@bot.message_handler(commands=['insert'])
def insert_command_handler(message):
    if db_u.in_database_checker(bot, message, message.from_user.id):
        message_content = message.text
        arg = u.extract_arg(message_content)
        if arg is not None:
            inserted_arg = db_u.pull_into_database(arg, message.from_user.id)
            bot.send_message(message.chat.id, "We got your transfer of " + inserted_arg + " UAH.")
        else:
            bot.send_message(message.chat.id, "Correct your input data to /insert 1032 format...")
    else:
        bot.send_message(message.chat.id, "You're not a roommate, to become a roommate - send /roommate...")


@bot.message_handler(commands=['balance'])
def balance_display(message):
    cursor = db_u.balance_counter()
    for result_object in cursor:
        bot.send_message(message.chat.id, "Totally right now we have " + str(result_object['total']) + " UAH. For more "
                                                                                                       "information "
                                                                                                       "about "
                                                                                                       "donations type "
                                                                                                       "/details.")


@bot.message_handler(commands=['details'])
def balance_detail_display(message):

    username_list, deposit_list = db_u.details_info_creator()
    reply_markup = u.keyboard_markup_setup(bot, message, username_list, deposit_list)
    reply_markup = json.loads(reply_markup)
    bot.send_message(message.chat.id, "All donations left: ", reply_markup=json.dumps(reply_markup))
    bot.send_message(message.chat.id, "Keep in mind, that changes won't be display here...")


@bot.message_handler(commands=['robbery'])
def purging_balance(message):
    if db_u.robbery():
        bot.send_message(message.chat.id, "All money got purged")
    else:
        bot.send_message(message.chat.id, "Something went wrong")


@bot.message_handler(commands=['spending'])
def spending_from_balance(message):
    telegram_id = message.from_user.id
    message_content = message.text
    spending = u.extract_arg(message_content)
    if spending is not None:
        shared_payment = db_u.deleting_from_deposit(spending)
        bot.send_message(message.chat.id, "Shared payment for all roommates will be around " + str(shared_payment) + ".")
        bot.send_message(message.chat.id, "Send receipt as well...")
    else:
        bot.send_message(message.chat.id, "Correct your input data to /spending 1032 format...")


@bot.message_handler(func=lambda m: True)
def text_message_handler(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        pass
    else:
        bot.send_message(message.chat.id, "You better use commands, I can't understand you anyway...")



bot.polling(NONE_STOP=True)
