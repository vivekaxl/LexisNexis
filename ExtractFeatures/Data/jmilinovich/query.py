from elasticsearch import Elasticsearch
import json

def getBooksByAuthor(es, author):
    q = """{
    "query": {
     "filtered": {
      "filter": {
       "term": {"author": "%(author)s"}
      }
     }
    }
    }
    """
    qry = q % dict(author=author)
    res = es.search(index='library', body=json.loads(qry))

    response = res['hits']['hits']

    if not len(response) > 0:
        print 'no books returned for %s' % author
        return ''
        
    return response
    

if __name__ == '__main__':
    es = Elasticsearch(host='localhost', port=9200)
    print json.dumps(getBooksByAuthor(es, 'Joe'))