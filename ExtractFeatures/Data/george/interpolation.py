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
import numpy as np
import TEAK

TREE_VERBOSE=False;
CLUSTER_ON_DECISION = False;

def launchInterpolate(m, dataset, rows=None,  CLUSTERER = launchWhere2, interpolationCount=1, clstrByDcsn=None):
  if (clstrByDcsn == None):
    tree = CLUSTERER(m, rows, verbose=TREE_VERBOSE)
  else :
    tree = CLUSTERER(m, rows, verbose=TREE_VERBOSE, clstrByDcsn = clstrByDcsn)
  interpolate(tree, dataset, interpolationCount)
  dataList = list(dataset.dataset)
  dataList = [list(dataList[i])for i in range(len(dataList))]
  return data(indep=INDEP, less= LESS, _rows=dataList, 
              _tunings=m._tunings, _doTune=m._doTune,
              _weighKLOC=m.weighKLOC, _klocWt=m.klocWt)

def interpolate(tree, dataset,interpolationCount=1):
  leaf_nodes = leaves(tree)
  for node in leaf_nodes:
    generateDuplicates(node[0].val, dataset,interpolationCount)

def generateDuplicates(rows, dataset,interpolationCount=1):
  maxSampling = (2**interpolationCount) * len(rows)
  sampleIndex = 0
  #max_cols, min_cols = getMinMax(rows)
  while (sampleIndex < maxSampling) :
    sampleIndex += 1
    randomSamples = random.sample(rows,2)
    dataset.dataset.add(createHybrid(randomSamples))
    
def createHybrid(originals):
  def mergeData(index):
    return x[index] + rNum * (max(x[index],y[index]) - min(x[index],y[index]))
  rNum = random.random()
  x = originals[0].cells
  y = originals[1].cells
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

def interpolateNTimes(initialModel, rows=None, CLUSTERER = launchWhere2, interpolationCount=1, clstrByDcsn=None):
  # interpolates the dataset to 2^(interpolationCount)
  random.seed(1)
  if  interpolationCount == 0:
    return initialModel
  initialModel = launchInterpolate(initialModel, ExtendedDataset(), rows, CLUSTERER, interpolationCount, clstrByDcsn)
  #launchWhere2(initialModel, verbose=True)
  return initialModel
  '''
  timesInterpolated = 0
  while timesInterpolated < interpolationCount:
    dataset = ExtendedDataset()
    if timesInterpolated != 0:
      rows=initialModel._rows
    initialModel = launchInterpolate(initialModel, dataset, rows)
    timesInterpolated += 1
  #print len(dataset)
  #launchWhere2(initialModel,verbose=True)
  return initialModel'''

#@go
def _interpolate():
   interpolateNTimes(nasa93(), interpolationCount=2)
