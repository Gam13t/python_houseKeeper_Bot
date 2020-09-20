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


def keyboard_markup_setup(bot, message):
    pass