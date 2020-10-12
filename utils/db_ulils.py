from models.database import Roommate


def pull_into_database(arg, telegram_id):
    Roommate.update_one({"Telegram_id": telegram_id},
                        {'$inc': {'Deposit': arg}})
    return str(arg)


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


def balance_counter():
    pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Deposit'}}}]
    cursor = Roommate.aggregate(pipeline=pipe)
    return cursor


def users_counter():
    usernames = []
    for doc in Roommate.find():
        usernames += [doc['Name']]
    return len(usernames)


def details_info_creator():
    usernames = []
    deposits = []
    for doc in Roommate.find():
        usernames += [doc['Name']]
        deposits += [doc['Deposit']]

    return usernames, deposits


def deleting_from_deposit(spending):
    users_among = users_counter()
    shared_payment = int(spending / users_among)
    try:
        Roommate.update_many({}, {"$inc": {"Deposit": (-1)*shared_payment}})
    except:
        print("Something went wrong...")

    return shared_payment


def robbery():
    try:
        Roommate.update_many({}, {"$set": {"Deposit": 0}})
        return True
    except:
        return False
