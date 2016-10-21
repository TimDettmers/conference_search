import cPickle as pickle
import sklearn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cdist
import gensim
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import WordPunctTokenizer


tokenizer = WordPunctTokenizer()


data = pickle.load(open('data.p','r'))

#paper abstract authors url title
abstracts = []
urls = []
titles = []
author_lists = []
tokens = []
for title, results in data:
    if results == None: continue

    (abstract, authors, url, title) = results
    authors = [author.strip().replace(' et al.', '') for author in authors if 'and' not in author]

    #print title, abstract, authors, url, title2
    abstracts.append(abstract.lower())
    urls.append(url)
    titles.append(title)
    author_lists.append(authors)
    tokens.append(tokenizer.tokenize(abstract.lower()))

tfidf = TfidfVectorizer(stop_words='english')
sents = []
for i, abstract in enumerate(tokens):
    print i
    sents.append(LabeledSentence(abstract, str(i)))


X = tfidf.fit_transform(abstracts).todense()
model = Doc2Vec(sents)

vecs = []
for i in range(X.shape[0]):
    vecs.append(model[str(i)])

vecs = np.array(vecs)
print vecs
print vecs
dists = cdist(X,X, 'euclidean')
print model.most_similar('1')
print abstracts[1]

similarities = []
for dist in dists:
    similarities.append(np.argsort(dist))


arxiv = 0
for paper in data:
    if paper[1]: arxiv +=1

print (arxiv*1.0)/(len(data))
