from bs4 import BeautifulSoup
import urllib2
import re
import cPickle as pickle

find_id = re.compile('r=(.*)&qid')


def get_abstract(url):
    webpage = urllib2.urlopen(url)
    soup = BeautifulSoup(webpage)
    return str(soup.find('blockquote').contents[2])


def get_url(query):
    webpage = urllib2.urlopen('http://search.arxiv.org:8081/?query={0}'.format(query))

    soup = BeautifulSoup(webpage)
    results = []
    for a in soup.find_all(True, ['author', 'title']):
        if a.has_attr('href'):
            results.append(a['href'])
        else:
            results.append(a.contents)

    for i, result in enumerate(results):
        if i % 3 == 2:
            joined = ''
            for c in result:
                joined += str(c)

            joined = joined.replace('<b>', '')
            joined = joined.replace('</b>', '')
            joined = joined.replace('\n', ' ')
            match = joined == query.replace('+', ' ')
            if match:
                authors = [str(author) for author in results[i-1]]
                url = 'https://arxiv.org/abs/{0}'.format(find_id.findall(results[i-2])[0])
                title = joined
                abstract = get_abstract(url)
                return [abstract, authors, url, title]
    print query
    return None



with open('emnlp.txt','r') as f:
    papers = f.readlines()

data = []
print round(len(papers)/3.0)
for i, line in enumerate(papers):
    if i % 3 == 0:
        print i
        results = get_url(line.rstrip().replace(' ','+'))
        data.append([line.rstrip(), results])


print data
pickle.dump(data, open('data.p','wb'), pickle.HIGHEST_PROTOCOL)


