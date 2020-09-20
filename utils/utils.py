# TODO: EXPAND utils by remaking some methods into abstractions

from models.database import Roommate
import pprint  # DEBUG


def extract_arg(arg, bot, message):
    arg_checker = arg.split()[1:]
    try:
        arg_checker = int(arg_checker[0])
        return arg_checker
    except:
        bot.send_message(message.chat.id, "Invalid input data...")
        return None


def keyboard_markup_setup(bot, message, username_list, deposits_list):
    reply_markup = "{\"inline_keyboard:["
    for i in range(len(username_list)):
        reply_markup += "[{\"text\": \"" + username_list[i] + " - " + str(deposits_list[i]) + "\", \"callback_data\": " \
                                                                                          "\"test1\"}], "
    reply_markup = reply_markup[:-2]
    reply_markup += "]}"
    return reply_markup

