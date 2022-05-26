from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater
import difflib
import linecache
import logging
import re


my_token = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
updater = Updater(token=my_token)
dispatcher = updater.dispatcher

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format, level=logging.INFO)


def string_polish(string: str) -> list:
    return sorted(string.strip("?").lower().split(" "))


def echo(update: Update, context: CallbackContext) -> None:
    best_match_value = matched_line = line_counter = rate = 0
    '''
    The following line formats the message recieved in such a way that it can be compared to the keyword in our file (SequenceMatcher is Case-Sensitive)
    The recieved line is cleaned of spaces, and ?, every word is then brought to lowercase
    Message also has to be ordered for sequenceMatcher to work properly since it looks at the LCS inside a string
    See function string_polish for details
    '''
    message = string_polish(update.message.text)
    with open("keywords.txt") as keyword_file:
        recoveredlist = keyword_file.readlines()

        for line in recoveredlist:
            #counter that keeps the current line number to store it later if best match
            line_counter += 1
            #SequenceMatcher returns a double that signifies the degree of similarity of two strings
            rate = difflib.SequenceMatcher(None, message, line.rstrip().split(" ")).ratio()
            #Finds best potential match ratio and line number
            if rate > best_match_value :
                best_match_value = rate
                matched_line = line_counter

    #Using a treshold to make sure there is a potential match
    #If ratio is sufficient recovers the line with best match
    if rate > 0.5: 
        final_mess = linecache.getline("corrispondence.txt", matched_line)
        context.bot.send_message(chat_id=update.effective_chat.id, text=final_mess)


echo_handler = MessageHandler(Filters.regex(r".*\?+.*"), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()