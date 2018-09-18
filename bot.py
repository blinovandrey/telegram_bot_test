import config
from functools import wraps

import telebot
from sqlalchemy.orm import sessionmaker
from telebot import types

from initdb import create_engine, get_db_config
from models import User
from utils import sort

TOKEN = config.TELEGRAM_TOKEN
bot = telebot.TeleBot(TOKEN)

db_config = get_db_config()
engine = create_engine(*db_config)

Session = sessionmaker(bind=engine)
session = Session()

users_dict = {}

user_template = u"id: {} \nfullname: {} \nage: {} \ngender: {} \ncity: {} \ncountry: {}\n\n"


@bot.message_handler(commands=['add'])
def add_user(message):
    msg = bot.reply_to(message, u"Enter user's fullname")
    bot.register_next_step_handler(msg, add_users_fullname)


def content_type_checker(func):
    @wraps(func)
    def wrapped(message):
        print message.content_type
        if message.content_type != 'text':
            msg = bot.reply_to(message, u"Message content must be text, not {}"
                               .format(message.content_type))
            bot.register_next_step_handler(msg, wrapped)
        else:
            func(message)
    return wrapped


@content_type_checker
def add_users_fullname(message):
    try:
        chat_id = message.chat.id
        user = User()
        user.set_fullname(message.text)
        users_dict[chat_id] = user
        msg = bot.reply_to(message, u"Enter user's age")
        bot.register_next_step_handler(msg, add_users_age)

    except Exception as e:
        msg = bot.reply_to(message, e.message)
        bot.register_next_step_handler(msg, add_users_fullname)


@content_type_checker
def add_users_age(message):
    try:
        chat_id = message.chat.id
        user = users_dict[chat_id]
        user.set_age(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*User.gender_list())
        msg = bot.reply_to(message, u"Select user's gender", reply_markup=markup)
        bot.register_next_step_handler(msg, add_users_gender)

    except Exception as e:
        msg = bot.reply_to(message, e.message)
        bot.register_next_step_handler(msg, add_users_age)


@content_type_checker
def add_users_gender(message):
    try:
        chat_id = message.chat.id
        user = users_dict[chat_id]
        user.set_gender(message.text)
        msg = bot.reply_to(message, u"Enter user's city")
        bot.register_next_step_handler(msg, add_users_city)

    except Exception as e:
        msg = bot.reply_to(message, e.message)
        bot.register_next_step_handler(msg, add_users_gender)


@content_type_checker
def add_users_city(message):
    try:
        chat_id = message.chat.id
        user = users_dict[chat_id]
        user.set_city(message.text)
        msg = bot.reply_to(message, u"Enter user's country")
        bot.register_next_step_handler(msg, add_users_country)

    except Exception as e:
        msg = bot.reply_to(message, e.message)
        bot.register_next_step_handler(msg, add_users_city)


@content_type_checker
def add_users_country(message):
    try:
        chat_id = message.chat.id
        user = users_dict[chat_id]
        user.set_country(message.text)
        session.add(user)
        session.commit()
        bot.reply_to(message, u"User successfully created! \n" + user_template
                     .format(user.id, user.fullname, user.age, user.gender.value, user.city, user.country))

    except Exception as e:
        msg = bot.reply_to(message, e.message)
        bot.register_next_step_handler(msg, add_users_country)


@bot.message_handler(commands=['del'])
def del_user(message):
    arg = message.text.split()[1]
    if not arg.isdigit():
        bot.reply_to(message, u"Argument must be number")
        return

    user = session.query(User).get(arg)
    if not user:
        bot.reply_to(message, u"User not found")
        return

    try:
        session.delete(user)
        session.commit()
        bot.reply_to(message, u"User successfully deleted!")
    except Exception as e:
        bot.reply_to(message, e.message)


@bot.message_handler(commands=['list'])
def list_users(message):
    try:
        users = session.query(User).all()
        msg = u"".join([user_template.format(
            user.id, user.fullname, user.age, user.gender.value, user.city, user.country) for user in sort(users)])
        bot.reply_to(message, msg)

    except Exception as e:
        bot.reply_to(message, e.message)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, u"Hello!")


bot.polling()
session.close()
