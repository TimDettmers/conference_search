import cPickle as pickle
import sklearn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cdist
import gensim
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import WordPunctTokenizer

data = pickle.load(open('data.p','r'))

class Dataset(object):
    def __init__(self):
        self.abstracts = []
        self.urls = []
        self.titles = []
        self.author_lists = []
        self.tokens = []
        self.tfidf_similarities = []
        self.word2vec_similarities  = []
        pass


    def preprocess_data(self):
        #paper abstract authors url title
        for title, results in data:
            if results == None: continue

            (abstract, authors, url, title) = results
            authors = [author.strip().replace(' et al.', '') for author in authors if 'and' not in author]

            #print title, abstract, authors, url, title2
            self.abstracts.append(abstract)
            self.urls.append(url)
            self.titles.append(title)
            self.author_lists.append(authors)
            self.tokens.append(tokenizer.tokenize(abstract.lower()))


    def process_tfidf(self):
        tokenizer = WordPunctTokenizer()




        tfidf = TfidfVectorizer(stop_words='english')
        X = tfidf.fit_transform(self.abstracts).todense()
        dists = cdist(X,X, 'euclidean')
        for dist in dists:
            self.tfidf_similarities.append(np.argsort(dist))


    def process_word2vec(self):
        dim = 200
        model = gensim.models.Word2Vec(iter=100,min_count=0,size=dim)  # an empty model, no training yet
        model.build_vocab(self.tokens, keep_raw_vocab=True)


        model.train(self.tokens)

        abstracts2vec = np.zeros((len(self.abstracts), dim))
        for i, abstract in enumerate(self.tokens):
            for token in abstract:
                if token in model.vocab:
                    abstracts2vec[i] += model[token]

        abstracts2vec /= float(len(self.abstracts))

        dists2 = cdist(abstracts2vec, abstracts2vec, 'euclidean')

        for dist in dists2:
            self.word2vec_similarities.append(np.argsort(dist))


