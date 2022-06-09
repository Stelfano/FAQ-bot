from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
import difflib
import linecache
import logging
import re
import random

#Token and bot id
MY_TOKEN = '5518198923:AAEl48PgQvBo175x-nws4SNFO7Xu6-bgY6s'
BOT_ID = '5518198923'
FORMAT_STRING = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=FORMAT_STRING, level=logging.INFO)


def string_polish(string: str) -> list:
    return sorted(string.strip("?").lower().split(" "))


def matcher(question: str) -> str:
    '''
    best_match_rate keeps the best rate of similarity between strings
    matched_line contains the line number with best match
    line_counter is just a simple counter used to keep the line number
    '''
    best_match_rate = matched_line = line_counter = 0
    '''
    The following line formats the message recieved in such a way that it can be compared to the keyword in our file (SequenceMatcher is Case-Sensitive)
    The recieved line is cleaned of spaces, and ?, every word is then brought to lowercase
    Message also has to be ordered for sequenceMatcher to work properly since it looks at the LCS inside a string
    See function string_polish for details
    '''
    message = string_polish(question)
    with open("keywords.txt") as keyword_file:
        recoveredlist = keyword_file.readlines()

        for line in recoveredlist:
            #counter that keeps the current line number to store it later if best match
            line_counter += 1
            #SequenceMatcher returns a double that signifies the degree of similarity of two strings
            rate = difflib.SequenceMatcher(None, message, line.rstrip().split(" ")).ratio()
            #Finds best potential match ratio and line number
            if rate > best_match_rate :
                best_match_rate = rate
                matched_line = line_counter

    #Using a treshold to make sure there is a potential match
    #If ratio is sufficient recovers the line with best match
    if best_match_rate > 0.5: 
        final_mess = linecache.getline("corrispondence.txt", matched_line)
        return final_mess




#First we define the essential: updater and dispatcher
updater = Updater(token = MY_TOKEN, use_context = True)

#This function is capable of reading the messages in the chat and subsequently answer them recalling the function "echo()"
#NOTE: it only identifies messages which:
#do not come from the bot;
#are not commands;
#have in their string the "?" character.

def autoresponse(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id = update.effective_chat.id,
    reply_to_message_id = update.message.message_id,
    text = matcher(update.message.text)
    )
 
autoresponse_handler = MessageHandler(Filters.regex(r".*\?+.*") & ~Filters.command,
        autoresponse)


dispatcher = updater.dispatcher
dispatcher.add_handler(autoresponse_handler)

updater.start_polling()
