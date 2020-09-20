from models.database import Roommate


def pull_into_database(arg, bot, message, telegram_id):
    Roommate.update_one({"Telegram_id": telegram_id},
                        {'$inc': {'Deposit': arg}})
    bot.send_message(message.chat.id, "We got your transfer of " + str(arg) + " UAH.")


def database_unique_user(bot, message, telegram_id):
    flag = Roommate.find_one({"Telegram_id": telegram_id})
    print(flag)
    if flag is not None:
        return False
    else:
        return True


def in_database_checker(bot, message, telegram_id):
    flag = Roommate.find_one({"Telegram_id": telegram_id})
    if flag is None:
        return False
    else:
        return True


def balance_counter(bot, message):
    pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Deposit'}}}]
    cursor = Roommate.aggregate(pipeline=pipe)
    for result_object in cursor:
        bot.send_message(message.chat.id, "Totally right now we have " + str(result_object['total']) + " UAH. For more "
                                                                                                       "information "
                                                                                                       "about "
                                                                                                       "donations type "
                                                                                                       "/details.")


def users_counter(bot, message):
    pass

