from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import linecache as lc

MY_TOKEN = '5518198923:AAEl48PgQvBo175x-nws4SNFO7Xu6-bgY6s'
BOT_ID = '5518198923'
FORMAT_STRING = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# logging.basicConfig(format=FORMAT_STRING, level=logging.INFO)


def matcher(question: str) -> str:
    tokenized_question = word_tokenize(question)
    stop_words = set(stopwords.words("italian"))
    fhand = open("keywords.txt", "r")
    stemming = nltk.wordnet.WordNetLemmatizer()

# We filter the question with unnecessary words and lemmatize to extract the
# meaning of a word
    filtered_question = [word for word in tokenized_question if word.casefold()
                         not in stop_words]
    filtered_question = [stemming.lemmatize(word) for word in
                         filtered_question]

# To determine which answer is the correct one we use values such
# as jaccard distance and other values
    min_jaccard = 1
    max_cust = 0
    best_match_line = 0

# Tresholds to prevent false positives
    jaccard_treshold = 0.3
    cust_treshold = 0.3

    for i in range(0, len(open('keywords.txt').readlines())):
        tokenized_answer = word_tokenize(fhand.readline())

# int_len is used as the length of the intersection between the two sets
# created from the lists of answer and question
        int_len = set(filtered_question).intersection(set(tokenized_answer))
        int_len = len(int_len)

        if int_len == 0:
            continue

# We compute jaccard distance and custom distance
        cust_sim = int_len/len(filtered_question)
        jaccard_dist = 1 - len(set(filtered_question))/int_len

# If the values go over the treshold we have got a potential match
        if (jaccard_dist < min_jaccard and cust_sim > max_cust and
                cust_sim > cust_treshold and jaccard_dist < jaccard_treshold):
            min_jaccard = jaccard_dist
            max_cust = cust_sim
            best_match_line = i

    if best_match_line != 0:
        return lc.getline("corrispondence.txt", best_match_line)


# First we define the essential: updater and dispatcher
updater = Updater(token=MY_TOKEN, use_context=True)

# This function is capable of reading the messages in the chat and
# subsequently answer them recalling the function "echo()"
# NOTE: it only identifies messages which:
# do not come from the bot;
# are not commands;
# have in their string the "?" character.


def autoresponse(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.message.message_id,
                             text=matcher(update.message.text)
                             )


autoresponse_handler = MessageHandler(Filters.regex(r".*\?+.*")
                                      & ~Filters.command, autoresponse)


dispatcher = updater.dispatcher
dispatcher.add_handler(autoresponse_handler)

updater.start_polling()
