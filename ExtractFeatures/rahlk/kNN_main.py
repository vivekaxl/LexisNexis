"""
German words! It's almost Oktober! :)
"""

from __future__ import division
from lib    import *
from demos  import *
from counts import *
from fi     import *
from table import *
from lib import isa
import numpy as np
import scipy as sp
import sys
from scipy.spatial.distance import pdist
sys.dont_write_bytecode = True
squareform = sp.spatial.distance.squareform

class o:
  def __init__(self, **d): self.__dict__.update(d)

class uberschrift:  # # German for header
  def __init__(self):
    pass

  def pairs(self, lst):
    for j in lst[0:]:
      last = j
      for i in lst[0:]:
        yield last, i

  def dist(self, lst1, lst2):
    def IB1(a, b):
      if not isinstance(a, bool) and not isinstance(a, str) or not isinstance(b, bool) and not isinstance(b, str): return (a - b) ** 2
      else: return not(a == b)
    return -np.sum([IB1(elem1, elem2) for elem1, elem2 in zip(lst1, lst2)])


class haupt:  # # Haupt translates roughly to main
  source = 'data/nasa93.csv'
  tbl = table(source)
  rows = map(lambda x :x.cells, tbl._rows)  # Get all the rows of the table
  uber = uberschrift();  # Create an alias for Uberschrift class.
  pairs = uber.pairs;  # Generate all possible combinations of data, I took the original pairs function and modified it slightly.
  pdistVect = []  # pairwise distance matrix.

  #--------------------------------------------------
  # When in doubt, test the kNN with the following list, CAUTION: Use 1 maybe 2 neighbors at most.
  # #rows=[[1,2],[1,3],[2,1],[3,1],[9,8],[10,9],[8,10]]
  #--------------------------------------------------

  for one, two in pairs(rows):
    # # Gets rid of the redundant values and prepares the matrix for a squareform.
    # # one>two gets only the lower triangle of the entire matrix, since the
    #  distance matrix is basically symmetric, this is all we need.
    if one > two:
      pdistVect.append(uber.dist(one, two))

  # Now get the square pairwise distance matrix. This is a MxM matrix, where M is the number of rows.
  # By the way, the pdistVect above is a M(M-1)/2 sized vector
  v = squareform(pdistVect)

  # # Do the actual k-NN ALgorithm
  for x in v:
    # # The actual KNN is pretty simple, we sort each row and obtain the first k closest indices.
    # Sorting thanks to http://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    sortedIndex = [i[0] for i in sorted(enumerate(x), key = lambda x:x[1], reverse = True)]
    sortedList = [i[1] for i in sorted(enumerate(x), key = lambda x:x[1], reverse = True)]
    print sortedList[1:6], sortedIndex[1:6]
    # # A quick note is in order-- We'll notice that 2 rows are not mutual neighbors, by that I mean
     # if ROW1 is a neighbor of ROW2, the reverse is not necessarily true. I think this is because
     # of the variety in each row, we have numbers, years, letters and symbols. Well..
  print '__________________________________'
