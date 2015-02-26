from __future__ import division,print_function
import  sys  
sys.dont_write_bytecode = True
#from lib import *
#from nasa93 import *

def sdiv(lst, tiny=2,cohen=0.3,
         num1=lambda x:x[0], num2=lambda x:x[1]):
  "Divide lst of (num1,num2) using variance of num2."
  #----------------------------------------------
  class Counts(): # Add/delete counts of numbers.
    def __init__(i,inits=[]):
      i.zero()
      for number in inits: i + number 
    def zero(i): i.n = i.mu = i.m2 = 0.0
    def sd(i)  : 
      if i.n < 2: return i.mu
      else:       
        return (max(0,i.m2)*1.0/(i.n - 1))**0.5
    def __add__(i,x):
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/(1.0*i.n)
      i.m2 += delta*(x - i.mu)
    def __sub__(i,x):
      if i.n < 2: return i.zero()
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)    

  #----------------------------------------------
  def divide(this,small): #Find best divide of 'this'
    lhs,rhs = Counts(), Counts(num2(x) for x in this)
    n0, least, cut = 1.0*rhs.n, rhs.sd(), None
    for j,x  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
        if maybe < least :  
          if abs(lhs.mu - rhs.mu) >= small:
            cut,least = j,maybe
      rhs - num2(x)
      lhs + num2(x)    
    return cut,least
  #----------------------------------------------
  def recurse(this, small,cuts):
    cut,sd = divide(this,small)
    if cut: 
      recurse(this[:cut], small, cuts)
      recurse(this[cut:], small, cuts)
    else:   
      cuts += [(sd * len(this)/len(lst),this)]
      #cuts += [(sd * len(this)/len(lst),[num2(row) for row in this])]
    return cuts
  #---| main |-----------------------------------
  small = Counts(num2(x) for x in lst).sd()*cohen
  if lst: 
    return recurse(sorted(lst,key=num1),small,[])

def cells(dataset, rows=None):
  if rows == None:
    rows = dataset._rows
  rowCells = []
  for row in rows:
    rowCells += [row.cells]
  return rowCells

def fss(d):
  rank = []
  maxVal, minVal = 0, sys.maxint
  for i in range(len(d.indep)):
    xs = sdiv(cells(d), 
              num1 = lambda x:x[i],
              num2 = lambda x:x[len(d.indep)])
    xpect = sum(map(lambda x: x[0],xs))
    if xpect < minVal:
      minVal = xpect
    elif xpect > maxVal:
      maxVal = xpect
    rank += [(xpect,i)]
  d.weights = normalize_weights(rank, maxVal, minVal)
  return d
  
def normalize_weights(rank, maxVal, minVal):
  # sort based on columns
  sortedRank = sorted(rank, key=lambda x: x[1])
  weights = []
  for value, dimension in sortedRank:
    # TODO Raise to power 2 and try
    normal_Wt= ((maxVal - value) / (maxVal - minVal))
    weights.append(normal_Wt)
  return weights;

  
#fss()