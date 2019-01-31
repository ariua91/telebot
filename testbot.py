import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import praw
import random
import datetime as dt

from config import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


updater = Updater(token=TELE_BOT_TOKEN)

dispatcher = updater.dispatcher

reddit = praw.Reddit("mememachine")
subs = ['dank_meme', 'memes', 'EdgyMemes', 'HistoryMemes', 'wholesomememes', 'dankchristianmemes']

def get_memes(sub, reddit, upper_b):
    """
    Get HOT memes from sub till the upper_b
    returns a random number
    """
    tmp = reddit.subreddit(sub)
    top_memes = tmp.hot(limit=upper_b)
    # should handle any error
    return random.sample(list(top_memes), 1)

def get_many_memes(subs, reddit, upper_b):
    """
    Get NEW memes from sub list till the upper_b
    """
    top_memes = {}
    for s in subs:
        tmp = reddit.subreddit(s)
        top_memes[s] = tmp.new(limit=upper_b)
    return top_memes

def get_date(created):
    return dt.datetime.fromtimestamp(created).replace(tzinfo=dt.timezone.utc)\
                                             .astimezone(tz=None) \
                                             + dt.timedelta(hours=8)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Welcome to dankness, fam."
    )

def echo(bot, update):
    echo_responses = ['Ooo, "{}", can you believe this guy?',
                      '"{}", you say?',
                      '''"{}"? Pull the other one, it's got bells on it.''',
                      'Stupid say "{}"?'
    ]
    bot.send_message(chat_id=update.message.chat_id,
                     text=random.choice(echo_responses).format(
                         update.message.text)
    )

def memes(bot, update):
    tmp_sub = random.choice(subs)
    tmp_meme = get_memes(tmp_sub, reddit, 15)[0]
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=tmp_meme.url,
        caption="{}\r\n\r\nfrom: {}\r\n{}".format(
            tmp_meme.title,
            tmp_sub,
            get_date(tmp_meme.created)
        )
    )

def many_memes(bot, update):
    top_meme = get_many_memes(subs, reddit, 5)
    for k, tmp in top_meme.items():
        for i in tmp:
            bot.send_photo(
                chat_id=update.message.chat_id,
                photo=i.url,
                caption="{}\r\n\r\nfrom: {}\r\n{}".format(
                    i.title,
                    k,
                    get_date(i.created)
                )
            )


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

meme_handler = CommandHandler('memes' ,memes)
dispatcher.add_handler(meme_handler)

many_memes_handler = CommandHandler('mememeupscotty', many_memes)
dispatcher.add_handler(many_memes_handler)

updater.start_polling()
