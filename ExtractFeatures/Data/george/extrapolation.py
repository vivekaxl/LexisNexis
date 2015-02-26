"""
Source file to perform interpolation on the nasa93 data
"""

import sys
import random
from lib import *
from Models.nasa93 import *
from settings import *
from where2 import *
from Utilities.utils import *
import time
import numpy as np

TREE_VERBOSE=False
USE_NEIGHBORS=True
CLUSTERER = launchWhere2

class Statics():
  neighborMap = dict()

def getTime():
  return round(time.time()*1000,4)
 
def launchExtrapolate(m, dataset, rows=None, extrapolationCount=1):
  Statics.neighborMap = dict()
  extrapolate(m, dataset, rows,extrapolationCount)
  dataList = list(dataset.dataset)
  dataList = [list(dataList[i])for i in range(len(dataList))]
  return data(indep=INDEP, less= LESS, _rows=dataList)
  
def getLeafNodes(tree):
  leafNodes = []
  for node in leaves(tree):
    leafNodes.append(node)
  return leafNodes

def getNeighborNodes(node):
  neighborNodes = Statics.neighborMap.get(id(node))
  if (neighborNodes):
    return neighborNodes
  neighborNodes = []
  for neigh_node in neighbors(node):
    neighborNodes.append(neigh_node)
  Statics.neighborMap[id(node)] = neighborNodes
  return neighborNodes

def extrapolate(m, dataset, rows=None,extrapolationCount=1):
  tree = CLUSTERER(m, rows=rows, verbose=TREE_VERBOSE)
  leaf_nodes = getLeafNodes(tree)
  if len(leaf_nodes)>0:
    max_extrapolation = (2**extrapolationCount)*len(m._rows)
    extrapolatiounCount = 0
    while extrapolationCount < max_extrapolation:
      if USE_NEIGHBORS :
        rClusters = randomNeighbors(leaf_nodes)     
      else :
        rClusters = random.sample(leaf_nodes,2)
      if (rClusters == None):
        continue
      generateDuplicates(rClusters[0][0].val, rClusters[0][0].val, dataset)
      #generateDuplicates(rClusters[0][0].val, rClusters[1][0].val, dataset)
      extrapolationCount += 1

def randomNeighbors(leaf_nodes):
  neighbor_leaves = getNeighborNodes(random.choice(leaf_nodes)[0])
  if (len(neighbor_leaves) == 0): 
    return None
  elif (len(neighbor_leaves) == 1):
    return [neighbor_leaves[0], neighbor_leaves[0]]
  else:
    return random.sample(neighbor_leaves,2)

def generateDuplicates(clusterA, clusterB, dataset):
  randChoice = random.choice([1,2])
  randElements = random.sample(clusterA,randChoice) + random.sample(clusterB, 3-randChoice)
  dataset.dataset.add(createHybrid(randElements))
    
def createHybrid(originals):
  def mergeData(index):
    return x[index] + rNum *(y[index] - z[index])
  rNum = random.random()
  x = originals[0].cells
  y = originals[1].cells
  z = originals[2].cells 
  hybrid = [mergeData(i) for i in range(len(x))]
  return tuple(formatDuplicate(hybrid))

def formatDuplicate(record):
  formatedRecord = []
  for i in range(len(record)):
    if DATATYPES[i] == int:
      formatedRecord.append(int(record[i]))
    else :
      formatedRecord.append(round(record[i],4))
  return formatedRecord

def getMinMax(rows):
  matrix = np.matrix(rows)
  max_cols = matrix.max(axis=0)
  min_cols = matrix.min(axis=0)
  return max_cols, min_cols

def extrapolateNTimes(initialModel, rows=None, extrapolationCount=1):
  # extrapolates the dataset to 2^(extrapolationCount)
  random.seed(1)
  if  extrapolationCount == 0:
    return initialModel
  initialModel = launchExtrapolate(initialModel, ExtendedDataset(), rows, extrapolationCount)
  '''
  timesExtrapolated = 0
  while timesExtrapolated < extrapolationCount:
    dataset = ExtendedDataset()
    if (timesExtrapolated != 0):
      rows = initialModel._rows
    initialModel = launchExtrapolate(initialModel, dataset, rows)
    timesExtrapolated += 1
  #print len(dataset)'''
  #launchWhere2(initialModel, verbose=True)
  return initialModel

#@go
def _extrapolate():
  extrapolateNTimes(nasa93(), extrapolationCount=2)

#@go
def _test():
  for k in range(1,10):
    startTime = getTime()  
    extrapolateNTimes(nasa93(), k)
    print(getTime()-startTime) 
