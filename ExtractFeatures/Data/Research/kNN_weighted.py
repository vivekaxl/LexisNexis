"""
German words! It's almost Oktober! :)
"""

from __future__ import division
from weights import *
from lib import isa
import numpy as np
import scipy as sp
import sys, sk
from scipy.spatial.distance import pdist
from scipy.interpolate.interpolate_wrapper import nearest
squareform=sp.spatial.distance.squareform
rdivDemo=sk.rdivDemo

sys.dont_write_bytecode = True

class uberschrift: ## German for header
  def __init__(self):
    pass
  
  def unwrap(self,t0):
    rows = map(lambda x :x.cells, t0._rows)
    H=[];
    for i in t0.headers:
      H.append(i.__dict__['name'])
    rows.insert(0,H)
    return {rows[0][z]:[p[z] for p in rows[1:] if z<=len(rows[1])-1] for z in xrange(0,len(rows[0]))}
        
  def pairs(self,lst):
    for j in lst[0:]:
      last = j
      for i in lst[0:]:
        yield last, i
      
  def dist(self, lst1, lst2, weights):
    def IB1(a,b,w):
      if not isinstance(a,bool) and not isinstance(a, str) or not isinstance(b,bool) and not isinstance(b, str): return w*(a-b)**2
      else: return w*(not a==b)
    return -np.sum([IB1(lst1[x], lst2[x], weight) for x, weight in enumerate(weights)])
  
  def mre(self, rows, depend, neighbours):
    #===========================================================================
    # MRE = (Want-Got)/Want
    #===========================================================================
    MRE=[]
    for i in xrange(len(rows)):
      Get = np.mean([rows[z][depend] for z in neighbours[i]])
      Want = rows[i][depend]
      MRE.append(abs((Want-Get)/(Want)))
    return MRE

class haupt: ## Haupt translates roughly to main
  source='data/nasa93.csv'
  tbl=table(source)
  rows = map(lambda x :x.cells, tbl._rows) # Get all the rows of the table
  uber=uberschrift(); # Create an alias for Uberschrift class.
  pairs = uber.pairs; # Generate all possible combinations of data, I took the original pairs function and modified it slightly.
  pdistVect=[] # pairwise distance matrix.
  pdistVect1=[] # pairwise distance matrix.
  w=weights()
  weights=w.weights(tbl)
  weightsEq=len(weights)*[1/len(weights)]
  depen=tbl.depen[0].__dict__['col']
  E=[]
  #--------------------------------------------------
  # When in doubt, test the kNN with the following list, CAUTION: Use 1 maybe 2 neighbors at most.
  ##rows=[[1,2],[1,3],[2,1],[3,1],[9,8],[10,9],[8,10]]
  #--------------------------------------------------
  
  for one, two in pairs(rows): 
    #==========================================================================
    # Gets rid of the redundant values and prepares the matrix for a squareform.
    # one>two gets only the lower triangle of the entire matrix, since the 
    # distance matrix is basically symmetric, this is all we need.
    #==========================================================================

    if one>two: 
      pdistVect.append(uber.dist(one, two, weightsEq))
      pdistVect1.append(uber.dist(one, two, weights))
  
  #=============================================================================
  # Now get the square pairwise distance matrix. This is a MxM matrix, where M is the number of rows.
  # By the way, the pdistVect above is a M(M-1)/2 sized vector
  #=============================================================================
  v=squareform(pdistVect)
  v1=squareform(pdistVect1)
  Neighbours=[]; nearestDist=[]
  Neighbours1=[]; nearestDist1=[]
  ## Do the actual k-NN ALgorithm
  for x in v:
    #===========================================================================
    # The actual KNN is pretty simple, we sort each row and obtain the first k closest indices.
    # Sorting thanks to http://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    #===========================================================================
    sortedIndex=[i[0] for i in sorted(enumerate(x), key=lambda x:x[1], reverse=True)]
    sortedList=[i[1] for i in sorted(enumerate(x), key=lambda x:x[1], reverse=True)]
    nearestDist.append(sortedList[1:6]), Neighbours.append(sortedIndex[1:6])

  for x in v1:
    #===========================================================================
    # The actual KNN is pretty simple, we sort each row and obtain the first k closest indices.
    # Sorting thanks to http://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    #===========================================================================
    sortedIndex=[i[0] for i in sorted(enumerate(x), key=lambda x:x[1], reverse=True)]
    sortedList=[i[1] for i in sorted(enumerate(x), key=lambda x:x[1], reverse=True)]
    nearestDist1.append(sortedList[1:6]), Neighbours1.append(sortedIndex[1:6])
  
  MRE =  uber.mre(rows, depen, Neighbours)  
  MRE.insert(0,'Before Weighting')
  E.append(MRE)
  MRE1 =  uber.mre(rows, depen, Neighbours1)  
  MRE1.insert(0,'After Weighting')
  E.append(MRE1)
  rdivDemo(E)
    #===========================================================================
    # A quick note is in order-- We'll notice that 2 rows are not mutual neighbor, by that I mean
    # if ROW1 is a neighbor of ROW2, the reverse is not necessarily true. I think this is because 
    # of the variety in each row, we have numbers, years, letters and symbols. Well..
    #===========================================================================
  print '_______________________________________________________________________'
  
    
  