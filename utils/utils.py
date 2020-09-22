# TODO: EXPAND utils by remaking some methods into abstractions
from config import ROOMMATE_PASSWORD


def extract_pass(password):
    pass_checker = password.split()[1:]
    try:
        pass_checker = str(pass_checker[0])
        return pass_checker
    except:
        return None


def extract_arg(arg):
    arg_checker = arg.split()[1:]
    try:
        arg_checker = int(arg_checker[0])
        return arg_checker
    except:
        return None


def keyboard_markup_setup(bot, message, username_list, deposits_list):
    reply_markup = "{\"inline_keyboard\":["
    for i in range(len(username_list)):
        reply_markup += "[{\"text\": \"" + username_list[i] + " - " + str(deposits_list[i]) + "\", \"callback_data\": " \
                                                                                          "\"dummydata\"}], "
    reply_markup = reply_markup[:-2]
    reply_markup += "]}"
    return reply_markup


def password_checker(arg):
    if arg == ROOMMATE_PASSWORD:
        return True
    else:
        return False
