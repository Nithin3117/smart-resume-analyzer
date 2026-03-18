import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    filtered = []

    for word in tokens:

        if word.isalpha() and word not in stopwords.words('english'):

            filtered.append(word)

    return filtered
