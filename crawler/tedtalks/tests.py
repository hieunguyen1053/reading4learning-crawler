from collections import Counter

from django.test import TestCase
from nltk import casual_tokenize
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger

# Create your tests here.

ner_tagger = StanfordNERTagger('/Users/hieunguyen/Coding/working/crawler/crawler/english.all.3class.distsim.crf.ser.gz',
                               '/Users/hieunguyen/Coding/working/crawler/crawler/stanford-ner.jar')


def filter_not_persons(tokens):
    tagged_tokens = ner_tagger.tag(tokens)
    return [token for token, tag in tagged_tokens if tag != 'PERSON']


def filter_not_number(tokens):
    def has_digit(token):
        return any(char.isdigit() for char in token)
    return [token for token in tokens if not has_digit(token)]


def filter_not_alphabet(tokens):
    def not_alphabet(token):
        return all(not char.isalpha() for char in token)
    return [token for token in tokens if not not_alphabet(token)]


def filter_stopwords(tokens):
    return [token for token in tokens if token.lower() not in stopwords.words('english')]


def get_word_count(text):
    tokens = casual_tokenize(text)
    tokens = filter_not_persons(tokens)
    tokens = filter_not_number(tokens)
    tokens = filter_not_alphabet(tokens)
    tokens = filter_stopwords(tokens)
    return Counter(tokens)
