#first we define the essential: updater and dispatcher

from telegram.ext import Updater
updater = Updater(token  = '<INSERIRE TOKEN DEL BOT (vedi BotFather)>',
        use_context = True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)

#defining the introductory function
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ParseMode

import random

#check whether this works just fine here or you got to move it lower the start function
updater.start_polling()

#this function is capable of reading the messages in the chat and subsequently answer them recalling the function "echo()"
#NOTE: it only identifies messages which:
#do not come from the bot;
#are not commands;
#have in their string the "?" character.

autoresponse_text = echo()

def autoresponse(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id = update.effective_chat.id,
    reply_to_message_id = message.message_id,
    text = autoresponse_text
    )

bot_id = <insert bot id from Telegram>
autoresponse_handler = MessageHandler(Filters.regex(r".*\?+.*") & ~Filters.command & ~Filters.user(bot_id),
        autoresponse)

dispatcher.add_handler(autoresponse_handler)

#http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagehandler.html
#https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.filters.html
