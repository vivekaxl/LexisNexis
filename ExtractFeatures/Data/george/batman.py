'''
SMOTE Experiments
'''

from __future__ import division,print_function
import sys
sys.path.extend(['/home/george/Panzer/Raise/Nasa 93'])
from random import seed, choice, random as rand
from math import ceil
from os import getcwd
import lib
from Models import *
from sdivUtil import sdiv, cells
from smote import smote

MODEL = Mystery1.Mystery1

def klazzify(model = MODEL(), rows = None):
  if rows == None:
    rows = model._rows
  
  def setKlazz(row, classID):
    for one in rows:
      if one.cells == row:
        one.classID = classID
        return one
  
  divisions = sdiv(cells(model, rows), 
        num1=lambda x:x[len(model.indep)],
        num2=lambda x:x[len(model.indep)])
  classIndex = 1
  model.classes = dict()
  for block in divisions:
    rowObjs = []
    for row in block[1]:
      rowObjs.append(setKlazz(row, classIndex))
    model.classes[classIndex] = rowObjs
    classIndex+=1  
  return model

def smotify(model=MODEL(), rows=None, k=5, factor = 100):
  if rows == None:
    rows = model._rows
    
  klazzify(model, rows)
  classLength = [len(model.classes[i]) for i in model.classes]
  maxLen, minLen = max(classLength), min(classLength)
  clones = []
  for key in model.classes:
    classLength = len(model.classes[key])
    f = factor
    if classLength < ((maxLen + minLen)/2) :
      f = (factor*(maxLen + minLen)/2)/classLength
    clones += smote(model, model.classes[key], k=k, N = int(ceil(f)))
  return clones

if __name__ == "__main__":  
  smotify(MODEL(weighFeature = True))