'''
Main File defining all the training logic
'''

from __future__ import division, print_function
import sys, random, re, settings
from lib import *
sys.dont_write_bytecode = True

def defOpts(**d):
  return o(
      decision = settings.CLASS_COL,
      delimeter = settings.DELIMITER,
      tokenizer = punktTokenizer,
      stemmer = porterStemmer,
      removeStops = True,
      learnRate = 0.1
  ).update(**d)


def popRows(file, opts=None):
  opts = opts or defOpts()
  def outputNormalizer(className):
    if  className == settings.SPAM:
      return 1
    else:
      return 0
  def lines():
    n=0;
    for line in open(file):
      cols = re.split(opts.delimeter, line.strip(), 1)
      cols[0] = outputNormalizer(cols[0])
      yield n, cols
      n += 1
  for n, cols in lines():
    # can add further logic here
    tokens, validTokens = opts.tokenizer(lower(cols[1]), opts.removeStops)
    cols[1] = validTokens
    cols.append(tokens)
    if opts.stemmer:
      cols[1] = opts.stemmer(cols[1])
      cols[2] = opts.stemmer(cols[2])
    yield n, cols

def tokenizer(line, tokenizingTerm= settings.TOKENIZER, case=lower):
  return re.sub(tokenizingTerm,"", case(line)).split()

def countWords(words):
  wordMap = {};
  for word in words:
    wordCount = wordMap.get(word) or 0
    wordCount += 1
    wordMap[word] = wordCount
  return wordMap

def readSpam(file='Dataset/SMSSpamCollection'):
  tokenizedList = [];
  for n, row in popRows(file):
    #wordMap = countWords(row[1])
    #scorekeeper.updateRecord(len(row[1]),row[1])
    tokenizedList.append(row)
  return tokenizedList  
 
  
def splitList(dataset):
  i=0
  while (i<10):
    i+=1
    shuffle(dataset)
  threshold = len(dataset)//5
  return dataset[:threshold], dataset[threshold:]
  
def TFIDF(dataset, scorekeeper):
  for row in dataset:
    wordMap = countWords(row[1])
    scorekeeper.updateRecord(len(row[1]),wordMap)
  scorekeeper.computeTFIDF()
  return scorekeeper.getWordsOnTFIDF()
    
def computeProbability(words, scorekeeper):
  wtSum = 0
  for word in words:
    wordInfo = scorekeeper.getWordInfo(word)
    if (not wordInfo):
      continue
    wtSum += wordInfo.weight
  exp = math.exp(wtSum)
  return exp/(1+exp)
  
def lrTrain(y, x, scorekeeper):
  opts = defOpts()
  wordMap = countWords(x)
  scorekeeper.updateRecord(len(x),wordMap)
  prob = computeProbability(x, scorekeeper)
  for word in x:
    newWt = scorekeeper.getWordInfo(word).weight + (y - prob)*opts.learnRate
    scorekeeper.updateWordWeight(word, newWt)

def lrTest(testDataSet, scorekeeper):
  confMatrix = o(TP=0, FP=0, FN=0, TN=0)
  for message in testDataSet:
    y = message[0]
    x = message[1]
    prob = computeProbability(x, scorekeeper)
    if ((y==1) and (prob >= 0.5)):
      confMatrix.TP+=1
    elif ((y==0) and (prob >= 0.5)):
      confMatrix.FP+=1
    elif ((y==1) and (prob < 0.5)):
      confMatrix.FN+=1
    else:
      confMatrix.TN+=1
  print(confMatrix)
  print(effeciency(confMatrix))
  
@go
def lrMain():
  seed()
  scorekeeper = ScoreKeeper()
  tokenizedList = readSpam()
  test, train = splitList(tokenizedList)
  for message in train:
    lrTrain(message[0], message[1], scorekeeper)
  lrTest(test, scorekeeper)