import cPickle as pickle

data = pickle.load(open('data.p','r'))


arxiv = 0
for paper in data:
    if paper[1]: arxiv +=1

print (arxiv*1.0)/(len(data))
