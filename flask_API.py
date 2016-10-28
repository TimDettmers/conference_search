'''
Created on Sep 29, 2014

@author: tim
'''
from flask import Flask
from flask import request
from flask import Response
from flask.ext.cors import CORS
import json
from crossdomain import crossdomain
import numpy as np
import cPickle as pickle
import embed
from flask import g



tfidf = pickle.load(open('tfidf.p'))
word2vec = pickle.load(open('word2vec.p'))
titles = pickle.load(open('titles.p'))
urls = pickle.load(open('urls.p'))

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/index', methods=['OPTIONS', 'GET', 'POST'])
@app.route('/', methods=['OPTIONS', 'GET', 'POST'])
@crossdomain(origin='*')
def test():
    def generate():
        for i in xrange(len(titles)):
            yield '<p><a href={1}>{0}</a></p>'.format(titles[i], urls[i])

    return Response(generate())


if __name__ == "__main__":   
    #app.run(host='0.0.0.0', port=5000,threaded=True, debug=True, use_reloader=True)
    app.run(host='127.0.0.1', port=5000,threaded=True, use_reloader=True)

    