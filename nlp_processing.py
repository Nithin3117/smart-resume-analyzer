import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# -------- SET NLTK DATA PATH --------
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

nltk.data.path.append(nltk_data_path)

# -------- DOWNLOAD REQUIRED DATA --------
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('punkt_tab', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)


# -------- PREPROCESS FUNCTION --------
def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [word for word in tokens if word not in string.punctuation]

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return tokens
