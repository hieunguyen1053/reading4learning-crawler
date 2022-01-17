import os

import lmdb

DIR = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(DIR, 'stemmer')

class Stemmer:
    def __init__(self, path=PATH):
        env = lmdb.open(
            path,
            max_readers=1,
            readonly=True,
            lock=False,
            readahead=False,
            meminit=False)
        self.txn = env.begin(write=False)

    def stem(self, word):
        word = word.lower()
        result = self.txn.get(word.encode())
        if result:
            return result.decode()
        return None


# env = lmdb.open('stemmer', map_size=int(1e12))
# cache = {}
# count = 0

# pbar = tqdm.tqdm(total=68626)

# reader = open('words.txt', 'r')
# for line in reader:
#     if line == '': continue
#     word1, word2 = line.split('\t')
#     word1 = word1.strip()
#     word2 = word2.strip()
#     if len(word2.split()) > 2: continue
#     cache[word1] = word2.encode()

#     count += 1
#     if count % 1000 == 0:
#         with env.begin(write=True) as txn:
#             for k, v in cache.items():
#                 txn.put(k.encode(), v)
#         cache.clear()
#         pbar.update(1000)

# with env.begin(write=True) as txn:
#     for k, v in cache.items():
#         txn.put(k.encode(), v)