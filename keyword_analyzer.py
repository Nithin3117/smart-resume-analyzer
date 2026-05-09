from collections import Counter
import re


def analyze_keywords(resume_text):

    # LOWERCASE
    text = resume_text.lower()

    # REMOVE SPECIAL CHARACTERS
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = text.split()

    # REMOVE COMMON WORDS
    stop_words = {

        "the", "and", "is", "in", "to",
        "of", "a", "for", "on", "with",
        "as", "an", "at", "by", "from"
    }

    filtered_words = [

        word for word in words

        if word not in stop_words and len(word) > 2
    ]

    # COUNT WORDS
    keyword_counts = Counter(filtered_words)

    # TOP 15
    top_keywords = keyword_counts.most_common(15)

    return top_keywords
