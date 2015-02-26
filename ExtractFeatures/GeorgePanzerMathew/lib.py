'''
Base File defining all the
classes and utility functions

Logic Courtesy: https://github.com/ai-se/timm/blob/master/genic.py
'''

from __future__ import division, print_function
import sys, random, settings, nltk, math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
sys.dont_write_bytecode = True

rand = random.random
seed = random.seed
shuffle = random.shuffle

stops = set(stopwords.words('english'))

def cached(f=None,cache={})	:
  "To keep the options, cache their last setting."
  if not f: 
    return cache
  def wrapper(**d)	:
    tmp = cache[f.__name__] = f(**d)
    return tmp
  return wrapper

class o(object):
  def __init__(i, **d):
    i.update(**d)
  def update(i, **d):
    i.__dict__.update(**d)
    return i
  def __repr__(i):
    def name(x)	:
      return x.__name__ if fun(x) else x
    d = i.__dict__
    show = [':%s=%s' % (k, name(d[k]))
            for k in sorted(d.keys())
            if k[0] is not '_']
    return '{' + ' '.join(show)+'}'

def shuffle(lst):
  random.shuffle(lst)
  return lst

def say(c):
  sys.stdout.write(str(c))

def fun(x):
  return x.__class__.__name__ == 'function'
	
def lower(x):
  return x.lower();

def upper(x):
  return x.upper();
	
def go(f):
  print("\n# ---|", f.__name__,"|-----------------")
  f()

'''
Returns tokenized list and 
(tokenized list - stopwords)

'''
def nltkTokenizer(x, removeStopwords = True):
  x = x.decode('ascii','ignore').encode('ascii')
  tokens = nltk.word_tokenize(x) 
  if not removeStopwords:
    return tokens, tokens
  validTokens = set(tokens).difference(stops)
  return list(tokens), list(validTokens)

def punktTokenizer(x, removeStopwords = True):
  x = x.decode('ascii','ignore').encode('ascii')
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(x)
  if not removeStopwords:
    return tokens, tokens
  validTokens = [token for token in tokens if token not in stops]
  #validTokens = set(tokens).difference(stops)
  return tokens, validTokens

def porterStemmer(words):
  stemmedList = list()
  stemmer = PorterStemmer()
  for word in words:
    stemmedList.append(stemmer.stem(word))
  return stemmedList

def effeciency(c):
  A,B,C,D = c.TN, c.FN, c.FP, c.TP
  e = o(precision=0, recall=0, 
        false_alarm=0, accuracy=0, 
        selectivity=0, neg_pos=0)
  e.recall = D/(B+D)
  e.false_alarm = C/(A+C)
  e.precision = D/(D+C)
  e.accuracy = (A+D)/(A+B+C+D)
  e.selectivity = (C+D)/(A+B+C+D)
  e.neg_pos = (A+C)/(B+D)
  return e
  
class Token(o):
  def __init__(i, name):
    super(Token, i).__init__(name=name, wordCount=0, docCount=0, TFIDF=0, weight=0)

class ScoreKeeper(o):
  def __init__(i):
    super(ScoreKeeper, i).__init__(words = 0, docs=0, wordScores={})
  
  def updateWord(i, name, wordCount):
    wordScore = i.wordScores.get(name)
    if not wordScore:
      wordScore = Token(name)
    wordScore.docCount += 1
    wordScore.wordCount += wordCount
    i.wordScores[name]=wordScore
  
  def updateRecord(i, wordsCount, wordsMap):
    i.words += wordsCount
    i.docs += 1
    for word in wordsMap:
      i.updateWord(word, wordsMap.get(word))
  
  def computeTFIDF(i):
    for word in i.wordScores:
      wordStat = i.wordScores.get(word)
      wordStat.TFIDF = i.TFIDF(wordStat.wordCount, wordStat.docCount)
      i.wordScores[word] = wordStat

  def TFIDF(i,wordCount, docCount):
    return wordCount/i.words * (i.docs/docCount)
  
  def getWordsOnTFIDF(i):
    scores = i.wordScores.values()
    sorted(scores, key=lambda token : token.TFIDF)
    return scores
  
  def getWordInfo(i, name):
    return i.wordScores.get(name)
  
  def updateWordWeight(i, name, weight):
    wordScore = i.wordScores.get(name)
    wordScore.weight = weight
    i.wordScores[name] = wordScore