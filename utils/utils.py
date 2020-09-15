# TODO: EXPAND utils by remaking some methods into abstractions

def extract_arg(arg, bot, message):
    arg_checker = arg.split()[1:]
    try:
        arg_checker = int(arg_checker[0])
        bot.send_message(message.chat.id, "We got your argument")
        return arg_checker
    except:
        bot.send_message(message.chat.id, "Invalid input data...")
        return None


def pull_into_database(arg, bot, message):
    pass


def database_unique_user(bot, message, telegram_id, Roommate):
    flag = Roommate.find_one({"Telegram_id": telegram_id})
    if flag is not None:
        return True
    else:
        return False
