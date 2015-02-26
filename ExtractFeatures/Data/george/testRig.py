from __future__ import division,print_function
import sys, random, math
import numpy as np
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LinearRegression
from lib import *
from where2 import *
import Technix.sk as sk
import Technix.CoCoMo as CoCoMo
import Technix.sdivUtil as sdivUtil
from Technix.smote import smote
from Technix.batman import smotify
from Technix.TEAK import teak, leafTeak
from Models import *
MODEL = usp05.usp05
"""
Creates a generator of 1 test record 
and rest training records
""" 
def loo(dataset):
  for index,item in enumerate(dataset):
    yield item, dataset[:index]+dataset[index+1:]

"""
### Printing Stuff
Print without newline:
Courtesy @timm
"""
def say(*lst): 
  print(*lst,end="")
  sys.stdout.flush()

def formatForCART(dataset,test,trains):
  indep = lambda x: x.cells[:len(dataset.indep)]
  dep   = lambda x: x.cells[len(dataset.indep)]
  trainInputSet = []
  trainOutputSet = []
  for train in trains:
    trainInputSet+=[indep(train)]
    trainOutputSet+=[dep(train)]
  return trainInputSet, trainOutputSet, indep(test), dep(test)

"""
Selecting the closest cluster and the closest row
""" 
def clusterk1(score, duplicatedModel, tree, test, desired_effort, leafFunc):
  test_leaf = leafFunc(duplicatedModel, test, tree)
  nearest_row = closest(duplicatedModel, test, test_leaf.val)
  test_effort = effort(duplicatedModel, nearest_row)
  error = abs(desired_effort - test_effort)/desired_effort
  #print("clusterk1", test_effort, desired_effort, error)
  score += error
  
def clustermean2(score, duplicatedModel, tree, test, desired_effort, leafFunc):
  test_leaf = leafFunc(duplicatedModel, test, tree)
  nearestN = closestN(duplicatedModel, 2, test, test_leaf.val)
  if (len(nearestN)==1) :
    nearest_row = nearestN[0][1]
    test_effort = effort(duplicatedModel, nearest_row)
    error = abs(desired_effort - test_effort)/desired_effort
  else :
    test_effort = sum(map(lambda x:effort(duplicatedModel, x[1]), nearestN[:2]))/2
    error = abs(desired_effort - test_effort)/desired_effort  
  score += error
  
def clusterWeightedMean2(score, duplicatedModel, tree, test, desired_effort, leafFunc):
  test_leaf = leafFunc(duplicatedModel, test, tree)
  nearestN = closestN(duplicatedModel, 2, test, test_leaf.val)
  if (len(nearestN)==1) :
    nearest_row = nearestN[0][1]
    test_effort = effort(duplicatedModel, nearest_row)
    error = abs(desired_effort - test_effort)/desired_effort
  else :
    nearest2 = nearestN[:2]
    wt_0, wt_1 = nearest2[1][0]/(nearest2[0][0]+nearest2[1][0]+0.00001) , nearest2[0][0]/(nearest2[0][0]+nearest2[1][0]+0.00001)
    test_effort = effort(duplicatedModel, nearest2[0][1])*wt_0 + effort(duplicatedModel, nearest2[1][1])*wt_1
    #test_effort = sum(map(lambda x:effort(duplicatedModel, x[1]), nearestN[:2]))/2
    error = abs(desired_effort - test_effort)/desired_effort  
  score += error
  
"""
Performing LinearRegression inside a cluster
to estimate effort
"""
def linRegressCluster(score, duplicatedModel, tree, test, desired_effort, leafFunc=leaf, doSmote=True):
  
  def getTrainData(rows):
    trainIPs, trainOPs = [], []
    for row in rows:
      #trainIPs.append(row.cells[:len(duplicatedModel.indep)])
      trainIPs.append([row.cosine])
      trainOPs.append(effort(duplicatedModel, row))
    return trainIPs, trainOPs
  
  def fastMapper(test_leaf, what = lambda duplicatedModel: duplicatedModel.decisions):
    data = test_leaf.val
    #data = smotify(duplicatedModel, test_leaf.val,k=5, factor=100)
    one  = any(data)             
    west = furthest(duplicatedModel,one,data, what = what)  
    east = furthest(duplicatedModel,west,data, what = what)
    c    = dist(duplicatedModel,west,east, what = what)
    test_leaf.west, test_leaf.east, test_leaf.c = west, east, c
    
    for one in data:
      if c == 0:
        one.cosine = 0
        continue
      a = dist(duplicatedModel,one,west, what = what)
      b = dist(duplicatedModel,one,east, what = what)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      one.cosine = x
      
  def getCosine(test_leaf, what = lambda duplicatedModel: duplicatedModel.decisions):
    if (test_leaf.c == 0):
      return 0
    a = dist(duplicatedModel,test,test_leaf.west, what = what)
    b = dist(duplicatedModel,test,test_leaf.east, what = what)
    return (a*a + test_leaf.c**2 - b*b)/(2*test_leaf.c) # cosine rule
    
  test_leaf = leafFunc(duplicatedModel, test, tree)
  #if (len(test_leaf.val) < 4) :
   # test_leaf = test_leaf._up
  if (len(test_leaf.val)>1) and doSmote:
    data = smote(duplicatedModel, test_leaf.val,k=5, N=100)
    linearRegression(score, duplicatedModel, data, test, desired_effort)
  else :
    fastMapper(test_leaf)
    trainIPs, trainOPs = getTrainData(test_leaf.val)
    clf = LinearRegression()
    clf.fit(trainIPs, trainOPs)
    test_effort = clf.predict(getCosine(test_leaf))
    error = abs(desired_effort - test_effort)/desired_effort
    score += error
  
  
"""
Performing LinearRegression over entire dataset
"""
def linearRegression(score, model, train, test, desired_effort):
  def getTrainData(rows):
    trainIPs, trainOPs = [], []
    for row in rows:
      trainIPs.append(row.cells[:len(model.indep)])
      trainOPs.append(effort(model, row))
    return trainIPs, trainOPs
  
  trainIPs, trainOPs = getTrainData(train)
  clf = LinearRegression()
  clf.fit(trainIPs, trainOPs)
  test_effort = clf.predict(test.cells[:len(model.indep)])
  error = abs(desired_effort - test_effort)/desired_effort
  score += error

"""
Selecting K-nearest neighbors and finding the mean
expected effort
"""
def kNearestNeighbor(score, duplicatedModel, test, desired_effort, k=1, rows = None):
  if rows == None:
    rows = duplicatedModel._rows
  nearestN = closestN(duplicatedModel, k, test, rows)
  test_effort = sorted(map(lambda x:effort(duplicatedModel, x[1]), nearestN))[k//2]
  score += abs(desired_effort - test_effort)/desired_effort  

"""
Classification and Regression Trees from sk-learn
"""
def CART(dataset, score, cartIP, test, desired_effort):
  trainIp, trainOp, testIp, testOp = formatForCART(dataset, test,cartIP);
  decTree = DecisionTreeClassifier(criterion="entropy", random_state=1)
  decTree.fit(trainIp,trainOp)
  test_effort = decTree.predict(testIp)[0]
  score += abs(desired_effort - test_effort)/desired_effort
  
def testRig(dataset=MODEL(), 
            doCART = False,doKNN = False, doLinRg = False):
  scores=dict(clstr=N(), lRgCl=N())
  if doCART:
    scores['CARTT']=N();
  if  doKNN:
    scores['knn_1'],scores['knn_3'],scores['knn_5'] = N(), N(), N()
  if doLinRg:
    scores['linRg'] = N()
  for score in scores.values():
    score.go=True
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    tree = launchWhere2(dataset, rows=train, verbose=False)
    n = scores["clstr"]
    n.go and clusterk1(n, dataset, tree, test, desired_effort, leaf)
    n = scores["lRgCl"]
    n.go and linRegressCluster(n, dataset, tree, test, desired_effort)
    if doCART:
      CART(dataset, scores["CARTT"], train, test, desired_effort)
    if doKNN:
      n = scores["knn_1"]
      n.go and kNearestNeighbor(n, dataset, test, desired_effort, k=1, rows=train)
      n = scores["knn_3"]
      n.go and kNearestNeighbor(n, dataset, test, desired_effort, k=3, rows=train)
      n = scores["knn_5"]
      n.go and kNearestNeighbor(n, dataset, test, desired_effort, k=5, rows=train)
    if doLinRg:
      n = scores["linRg"]
      n.go and linearRegression(n, dataset, train, test, desired_effort)
  return scores
  
"""
Test Rig to test CoCoMo for
a particular dataset
"""
def testCoCoMo(dataset=MODEL(), a=2.94, b=0.91):
  scores = dict(COCOMO2 = N(), COCONUT= N())
  tuned_a, tuned_b = CoCoMo.coconut(dataset, dataset._rows)
  for score in scores.values():
    score.go=True
  for row in dataset._rows:
    #say('.')
    desired_effort = effort(dataset, row)
    test_effort = CoCoMo.cocomo2(dataset, row.cells, a, b)
    test_effort_tuned = CoCoMo.cocomo2(dataset, row.cells, tuned_a, tuned_b)
    scores["COCOMO2"] += abs(desired_effort - test_effort)/desired_effort
    scores["COCONUT"] += abs(desired_effort - test_effort_tuned)/desired_effort
  return scores
        
    
def testDriver():
  seed(0)
  skData = []
  split = "median"
  dataset=MODEL(split=split)
  if  dataset._isCocomo:
    scores = testCoCoMo(dataset)
    for key, n in scores.items():
      skData.append([key+".       ."] + n.cache.all)
  scores = testRig(dataset=MODEL(split=split),doCART = True, doKNN=True, doLinRg=True)
  for key,n in scores.items():
    if (key == "clstr" or key == "lRgCl"):
      skData.append([key+"(no tuning)"] + n.cache.all)
    else:
      skData.append([key+".         ."] + n.cache.all)

  scores = testRig(dataset=MODEL(split=split, weighFeature = True), doKNN=True)
  for key,n in scores.items():
      skData.append([key+"(sdiv_wt^1)"] + n.cache.all)
  scores = dict(TEAK=N())
  for score in scores.values():
    score.go=True
  dataset=MODEL(split=split)
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    tree = teak(dataset, rows = train)
    n = scores["TEAK"]
    n.go and clusterk1(n, dataset, tree, test, desired_effort, leafTeak)
  for key,n in scores.items():
      skData.append([key+".          ."] + n.cache.all)
  print("")
  print(str(len(dataset._rows)) + " data points,  " + str(len(dataset.indep)) + " attributes")
  print("")
  sk.rdivDemo(skData)
  #launchWhere2(MODEL())
  
#testDriver()

def testKLOCWeighDriver():
  dataset = MODEL(doTune=False, weighKLOC=True)
  tuneRatio = 0.9
  skData = [];
  while(tuneRatio <= 1.2):
    dataset.tuneRatio = tuneRatio
    scores = testRig(dataset=dataset)
    for key,n in scores.items():
      skData.append([key+"( "+str(tuneRatio)+" )"] + n.cache.all)
    tuneRatio += 0.01
  print("")
  sk.rdivDemo(skData)

#testKLOCWeighDriver()

def testKLOCTuneDriver():
  tuneRatio = 0.9
  skData = [];
  while(tuneRatio <= 1.2):
    dataset = MODEL(doTune=True, weighKLOC=False, klocWt=tuneRatio)
    scores = testRig(dataset=dataset)
    for key,n in scores.items():
      skData.append([key+"( "+str(tuneRatio)+" )"] + n.cache.all)
    tuneRatio += 0.01
  print("")
  sk.rdivDemo(skData)
  
#testKLOCTuneDriver()

#testRig(dataset=MODEL(doTune=False, weighKLOC=False), duplicator=interpolateNTimes)

def testOverfit(dataset= MODEL(split="median")):
  skData = [];
  scores= dict(splitSize_2=N(),splitSize_4=N(),splitSize_8=N())
  for score in scores.values():
    score.go=True
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    tree = launchWhere2(dataset, rows=train, verbose=False, minSize=2)
    n = scores["splitSize_2"]
    n.go and linRegressCluster(n, dataset, tree, test, desired_effort)
    tree = launchWhere2(dataset, rows=train, verbose=False, minSize=4)
    n = scores["splitSize_4"]
    n.go and linRegressCluster(n, dataset, tree, test, desired_effort)
    tree = launchWhere2(dataset, rows=train, verbose=False, minSize=8)
    n = scores["splitSize_8"]
    n.go and linRegressCluster(n, dataset, tree, test, desired_effort)
  
  for key,n in scores.items():
      skData.append([key] + n.cache.all)
  print("")
  sk.rdivDemo(skData)
  
#testOverfit()

def testSmote():
  dataset=MODEL(split="variance", weighFeature=True)
  launchWhere2(dataset, verbose=False)
  skData = [];
  scores= dict(sm_knn_1_w=N(), sm_knn_3_w=N(), CART=N())
  for score in scores.values():
    score.go=True
  
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    clones = smotify(dataset, train,k=5, factor=100)
    n = scores["CART"]
    n.go and CART(dataset, scores["CART"], train, test, desired_effort)
    n = scores["sm_knn_1_w"]
    n.go and kNearestNeighbor(n, dataset, test, desired_effort, 1, clones)
    n = scores["sm_knn_3_w"]
    n.go and kNearestNeighbor(n, dataset, test, desired_effort, 3, clones)
  
  for key,n in scores.items():
    skData.append([key] + n.cache.all)
  if dataset._isCocomo:
    for key,n in testCoCoMo(dataset).items():
      skData.append([key] + n.cache.all)
  
  scores= dict(knn_1=N(), knn_3=N())
  dataset=MODEL(split="variance", weighFeature=True)
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    n = scores["knn_1_w"]
    kNearestNeighbor(n, dataset, test, desired_effort, 1, train)
    n = scores["knn_3_w"]
    kNearestNeighbor(n, dataset, test, desired_effort, 3, train)
  for key,n in scores.items():
    skData.append([key] + n.cache.all)
    
  scores= dict(knn_1_w=N(), knn_3_w=N())
  dataset=MODEL(split="variance")
  for test, train in loo(dataset._rows):
    say(".")
    desired_effort = effort(dataset, test)
    n = scores["knn_1"]
    kNearestNeighbor(n, dataset, test, desired_effort, 1, train)
    n = scores["knn_3"]
    kNearestNeighbor(n, dataset, test, desired_effort, 3, train)
  for key,n in scores.items():
    skData.append([key] + n.cache.all)
    
  print("")
  sk.rdivDemo(skData)
  
def testForPaper(model=MODEL):
  split="median"
  print(model.__name__.upper())
  dataset=model(split=split, weighFeature=False)
  print(str(len(dataset._rows)) + " data points,  " + str(len(dataset.indep)) + " attributes")
  dataset_weighted = model(split=split, weighFeature=True)
  launchWhere2(dataset, verbose=False)
  skData = []
  if dataset._isCocomo:
    for key,n in testCoCoMo(dataset).items():
      skData.append([key] + n.cache.all)
  scores = dict(CART = N(), knn_1 = N(),
                knn_3 = N(),LSR = N(), 
                wt_clstr_wdMn2=N())
  for score in scores.values():
    score.go=True
  for test, train in loo(dataset._rows):
    desired_effort = effort(dataset, test)
    tree = launchWhere2(dataset, rows=train, verbose=False)
    n = scores["LSR"]
    n.go and linearRegression(n, dataset, train, test, desired_effort)
    n = scores["CART"]
    n.go and CART(dataset, scores["CART"], train, test, desired_effort)
    n = scores["knn_1"]
    n.go and kNearestNeighbor(n, dataset, test, desired_effort, 1, train)
    n = scores["knn_3"]
    n.go and kNearestNeighbor(n, dataset, test, desired_effort, 3, train)
  
  for test, train in loo(dataset_weighted._rows):
    desired_effort = effort(dataset, test)
    tree_weighted, leafFunc = launchWhere2(dataset_weighted, rows=train, verbose=False), leaf
    n = scores["wt_clstr_wdMn2"]
    n.go and clusterWeightedMean2(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
  
  for key,n in scores.items():
    skData.append([key] + n.cache.all)
  
  print("")
  sk.rdivDemo(skData)
  print("");print("")
    
  
def testEverything(model = MODEL):
  split="median"
  print(model.__name__.upper())
  dataset=model(split=split, weighFeature=False)
  print(str(len(dataset._rows)) + " data points,  " + str(len(dataset.indep)) + " attributes")
  dataset_weighted = model(split=split, weighFeature=True)
  launchWhere2(dataset, verbose=False)
  skData = [];
  scores= dict(TEAK=N(), linear_reg=N(), CART=N(),
               linRgCl_wt=N(), clstr_whr_wt=N(),
               linRgCl=N(), clstr_whr=N(),
               t_linRgCl_wt=N(), t_clstr_whr_wt=N(),
               knn_1=N(), knn_1_wt=N(), 
               clstrMn2=N(), clstrMn2_wt=N(), t_clstrMn2_wt=N(),
               clstrWdMn2=N(), clstrWdMn2_wt=N(), t_clstrWdMn2_wt=N())
  #scores= dict(TEAK=N(), linear_reg=N(), linRgCl=N())
  for score in scores.values():
    score.go=True
  for test, train in loo(dataset._rows):
    #say(".")
    desired_effort = effort(dataset, test)
    tree = launchWhere2(dataset, rows=train, verbose=False)
    tree_teak = teak(dataset, rows = train)
    n = scores["TEAK"]
    n.go and clusterk1(n, dataset, tree_teak, test, desired_effort, leafTeak)
    n = scores["linear_reg"]
    n.go and linearRegression(n, dataset, train, test, desired_effort)
    n = scores["clstr_whr"]
    n.go and clusterk1(n, dataset, tree, test, desired_effort, leaf)
    n = scores["linRgCl"]
    n.go and linRegressCluster(n, dataset, tree, test, desired_effort, leaf)
    n = scores["knn_1"]
    n.go and kNearestNeighbor(n, dataset, test, desired_effort, 1, train)
    n = scores["clstrMn2"]
    n.go and clustermean2(n, dataset, tree, test, desired_effort, leaf)
    n = scores["clstrWdMn2"]
    n.go and clusterWeightedMean2(n, dataset, tree, test, desired_effort, leaf)
    n = scores["CART"]
    n.go and CART(dataset, scores["CART"], train, test, desired_effort)
    
  for test, train in loo(dataset_weighted._rows):
    #say(".")
    desired_effort = effort(dataset_weighted, test)
    
    tree_weighted, leafFunc = launchWhere2(dataset_weighted, rows=train, verbose=False), leaf
    n = scores["clstr_whr_wt"]
    n.go and clusterk1(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    n = scores["linRgCl_wt"]
    n.go and linRegressCluster(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc=leafFunc)
    n = scores["clstrMn2_wt"]
    n.go and clustermean2(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    n = scores["clstrWdMn2_wt"]
    n.go and clusterWeightedMean2(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    
    tree_weighted, leafFunc = teak(dataset_weighted, rows=train, verbose=False),leafTeak
    n = scores["t_clstr_whr_wt"]
    n.go and clusterk1(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    n = scores["t_linRgCl_wt"]
    n.go and linRegressCluster(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc=leafFunc)
    n = scores["knn_1_wt"]
    n.go and kNearestNeighbor(n, dataset_weighted, test, desired_effort, 1, train)
    n = scores["t_clstrMn2_wt"]
    n.go and clustermean2(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    n = scores["t_clstrWdMn2_wt"]
    n.go and clusterWeightedMean2(n, dataset_weighted, tree_weighted, test, desired_effort, leafFunc)
    
  for key,n in scores.items():
    skData.append([key] + n.cache.all)
  if dataset._isCocomo:
    for key,n in testCoCoMo(dataset).items():
      skData.append([key] + n.cache.all)  
  print("")
  sk.rdivDemo(skData)
  print("");print("")

  
def runAllModels(test_name):
  models = [nasa93.nasa93, coc81.coc81, Mystery1.Mystery1, Mystery2.Mystery2,
            albrecht.albrecht, kemerer.kemerer, kitchenham.kitchenham,
           maxwell.maxwell, miyazaki.miyazaki, telecom.telecom, usp05.usp05,
           china.china, cosmic.cosmic, isbsg10.isbsg10]
  for model in models:
    test_name(model)
    


if __name__ == "__main__":
  #testForPaper(nasa93.nasa93)
  runAllModels(testForPaper)
