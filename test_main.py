#THIS FILE CONTAINS A COPY OF THE FUNCTION IMPLEMENTED IN main.py FILE
#IF YOU WISH TO ESPAND / FIX MATCHER, PLEASE NOTE THAT THIS FILE HERE
#NEEDS TO BE CHANGED TOO
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import linecache as lc


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

def test_matcher():
    assert matcher("appello algoritmi?")
    assert matcher("appello interazione e multimedia?")
    assert matcher("appello data mining?")
