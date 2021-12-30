from collections import Counter

from nltk import casual_tokenize
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger

ner_tagger = StanfordNERTagger('tools/english.all.3class.distsim.crf.ser.gz',
                               'tools/stanford-ner.jar')


def filter_not_persons_and_organizations(tokens):
    tagged_tokens = ner_tagger.tag(tokens)
    return [token for token, tag in tagged_tokens if tag != 'PERSON' and tag != 'ORGANIZATION']


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


def to_statistics_str(counter):
    result = ''
    for word, count in counter.items():
        result += '{}\t{}\n'.format(word, count)
    return result


def get_word_count(text):
    tokens = casual_tokenize(text)
    tokens = filter_not_persons_and_organizations(tokens)
    tokens = filter_not_number(tokens)
    tokens = filter_not_alphabet(tokens)
    tokens = filter_stopwords(tokens)
    counter = Counter(tokens)
    return to_statistics_str(counter)
