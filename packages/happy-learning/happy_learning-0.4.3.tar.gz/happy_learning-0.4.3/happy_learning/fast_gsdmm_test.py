import numpy as np
import pandas as pd
import re
import pickle
import itertools
from datetime import datetime

from happy_learning.text_clustering import GibbsSamplingDirichletMultinomialModeling

#tweets_df = pd.read_csv('/Users/giannibalistreri/Downloads/gsdmm-master/preprocessed_tweets.csv', sep=',')
tweets_df = pd.read_csv('/Users/giannibalistreri/Downloads/training_data_set.csv', sep='\t')
# convert string of tokens into tokens list
tweets_df['text'] = tweets_df['text'].apply(lambda x: str(x).replace('  ', ''))
tweets_df['text_tokenized'] = tweets_df['text'].apply(lambda x: re.split('\s', str(x)))
#tweets_df['text_tokenized'] = tweets_df['text'].apply(lambda x: x.split(' '))
# create list of  token lists
#docs = tweets_df['tokens'].tolist()
docs = tweets_df['text_tokenized'].tolist()
tweets_df.head(20)

print(datetime.now())
vocab = list(set(x for doc in docs for x in doc))
#print('Vocab', vocab)
n_terms = len(vocab)
mgp = GibbsSamplingDirichletMultinomialModeling(vocab=vocab, n_clusters=6, alpha=0.1, beta=0.5, n_iterations=5)
print('Terms:', n_terms)
y = mgp.fit(docs)
print(datetime.now())
