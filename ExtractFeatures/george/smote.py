from __future__ import division,print_function
import sys
sys.path.extend(['/home/george/Panzer/Raise/Nasa 93'])
import copy
sys.dont_write_bytecode = True
from lib import *
from random import seed, choice, random as rand
from Models import *
from where2 import closestN

MODEL = nasa93.nasa93

def smote(dataset=MODEL(), rows = None, k=3, N = 4):
  """
  Creates a generator of 1 test record 
  and rest training records
  """
  clones = []
  
  def loo(dataset):
    for index,item in enumerate(dataset):
      yield item, dataset[:index]+dataset[index+1:]
  
  def formatCells(one):
    if not dataset.dataTypes:
      return
    for i, a in enumerate(one.cells):
      one.cells[i] = dataset.dataTypes[i](a)
  
  def clone(one, two):
    new = copy.deepcopy(one)
    if not dataset.dataTypes:
      new.cells = [min(x,y) + rand()*(abs(x-y))
                for x, y in zip(one.cells, two.cells)]
    else :
      new.cells = [dataset.dataTypes[i](min(x,y) + rand()*(abs(x-y)))
                  for i,x, y in 
                    zip(range(0,len(one.cells)), one.cells, two.cells)]
    return new
  
  def populate(one, rest):
    nearestN = closestN(dataset, k, one, rest)
    for i in range(0,N):
      dist, neighbor = choice(nearestN)
      clones.append(clone(one, neighbor))
    
  seed()
  if not rows:
    rows = dataset._rows
  for one, rest in loo(rows):
    populate(one, rest)
  return clones
    
if __name__ == "__main__":
  smote(MODEL())