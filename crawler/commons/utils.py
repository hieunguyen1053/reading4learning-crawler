import re
from collections import Counter

from nltk import casual_tokenize


def filter_not_number(tokens):
    def has_digit(token):
        return any(char.isdigit() for char in token)
    return [token for token in tokens if not has_digit(token)]


def filter_not_alphabet(tokens):
    def not_alphabet(token):
        return all(not char.isalpha() for char in token)
    return [token for token in tokens if not not_alphabet(token)]


def remove_url(text):
    url = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
    return re.sub(url, '', text)


def remove_hashtag(text):
    hashtag = '((\#|\@)[a-zA-Z]+)'
    return re.sub(hashtag, '', text)


def remove_reference(text):
    pattern = '\[\d+ \w+\]'
    return re.sub(pattern, '', text)


def remove_tag(text):
    pattern = '\!\#h\d\#\!'
    return re.sub(pattern, '', text)


def normalize(text):
    text = re.sub("'s", ' is', text)
    text = re.sub("'ve", ' have', text)
    text = re.sub("'re", ' are', text)
    text = re.sub("'d", ' would', text)
    text = re.sub("'ll", ' will', text)
    text = re.sub("'m", ' am', text)
    text = re.sub("n't", ' not', text)
    return text


def to_statistics_str(counter):
    result = ''
    for word, count in counter.items():
        result += '{}\t{}\n'.format(word, count)
    return result


def get_word_count(text):
    text = normalize(text)
    text = remove_url(text)
    text = remove_hashtag(text)
    text = remove_reference(text)
    text = remove_tag(text)
    tokens = casual_tokenize(text)
    tokens = filter_not_number(tokens)
    tokens = filter_not_alphabet(tokens)
    counter = Counter(tokens)
    return to_statistics_str(counter)
