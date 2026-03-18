import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess(text):

    # convert text to lowercase
    text = text.lower()

    # split text into words
    tokens = word_tokenize(text)

    # remove unnecessary words
    filtered_words = []

    for word in tokens:
        if word.isalpha() and word not in stopwords.words('english'):
            filtered_words.append(word)

    return filtered_words