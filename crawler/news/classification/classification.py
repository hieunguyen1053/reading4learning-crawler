import os
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer

from ..models import Category

DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = [filename.split('.')[0] for filename in os.listdir(DIR + '/bin/svm') if filename.endswith('.pkl')]


class Classification:
    def __init__(self):
        self.categories = [category for category in Category.objects.all() if category.name in CATEGORIES]

        self.category_moduls = {category: {} for category in self.categories}
        for category in self.categories:
            tfidf_transformer, vocab = self.load_tfidf(f'{DIR}/bin/features/{category.name}.idf')
            self.category_moduls[category]['tfidf_transformer'] = tfidf_transformer
            self.category_moduls[category]['vocab'] = vocab
            self.category_moduls[category]['svm'] = self.load_svm(f'{DIR}/bin/svm/{category.name}.pkl')

    def load_tfidf(self, tfidf_path):
        vocab = {}
        with open(tfidf_path) as f:
            for line in f:
                line = line.strip()
                word, idf = line.split('\t')
                vocab[word] = float(idf)
        tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        tfidf_transformer.idf_ = [vocab[word] for word in vocab]
        return tfidf_transformer, vocab

    def load_svm(self, svm_path):
        return pickle.load(open(svm_path, 'rb'))

    def classify(self, counter):
        result = []
        for category in self.categories:
            vocab = self.category_moduls[category]['vocab']
            token2idx = {word: idx for idx, word in enumerate(vocab)}
            vector = np.zeros((1, len(self.category_moduls[category]['vocab'])))
            for token in counter:
                if token in vocab:
                    vector[0, token2idx[token]] = counter[token]
            tfidf_transformer = self.category_moduls[category]['tfidf_transformer']
            vector = tfidf_transformer.transform(vector)
            svm = self.category_moduls[category]['svm']
            pred = svm.predict_proba(vector)[0]
            idx = np.argmax(pred)
            prob = pred[idx]

            if idx == 1 and prob > 0.85:
                result.append(category)

        result += [category.parent for category in result if category.parent]
        result = list(set(result))
        return result
