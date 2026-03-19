import string

def preprocess(text):

    # Convert to lowercase
    text = text.lower()

    # Simple tokenization (split by spaces)
    tokens = text.split()

    # Remove punctuation
    tokens = [word.strip(string.punctuation) for word in tokens]

    # Remove empty tokens
    tokens = [word for word in tokens if word != ""]

    # Simple stopwords list
    stop_words = {
        "the", "and", "is", "in", "to", "of", "for", "on", "with",
        "as", "by", "an", "at", "from", "or", "that", "this",
        "it", "be", "are", "was", "were"
    }

    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    return tokens
