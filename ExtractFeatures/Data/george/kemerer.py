"""
# https://code.google.com/p/promisedata/source/browse/#svn%2Ftrunk%2Feffort%2Falbrecht

Standard header:

"""
from __future__ import division,print_function
import  sys
sys.dont_write_bytecode = True
from lib import *

"""
@attribute Language numeric
@attribute Hardware numeric
@attribute Duration numeric
@attribute KSLOC numeric
@attribute AdjFP numeric
@attribute RAWFP numeric
@attribute EffortMM numeric
"""

def kemerer(weighFeature = None, 
           split = "variance"):
  vl=1;l=2;n=3;h=4;vh=5;xh=6;_=0
  return data(indep= [ 
     # 0..5
     'Language','Hardware','Duration','KSLOC','AdjFP','RAWFP'],
    less = ['Effort'],
    _rows=[
      [1,1,17,253.6,1217.1,1010,287],
      [1,2,7,40.5,507.3,457,82.5],
      [1,3,15,450,2306.8,2284,1107.31],
      [1,1,18,214.4,788.5,881,86.9],
      [1,2,13,449.9,1337.6,1583,336.3],
      [1,4,5,50,421.3,411,84],
      [2,4,5,43,99.9,97,23.2],
      [1,2,11,200,993,998,130.3],
      [1,1,14,289,1592.9,1554,116],
      [1,1,5,39,240,250,72],
      [1,1,13,254.2,1611,1603,258.7],
      [1,5,31,128.6,789,724,230.7],
      [1,6,20,161.4,690.9,705,157],
      [1,1,26,164.8,1347.5,1375,246.9],
      [3,1,14,60.2,1044.3,976,69.9]
    ],
    _tunings =[[
    #         vlow  low   nom   high  vhigh xhigh
    #scale factors:
    'Prec',   6.20, 4.96, 3.72, 2.48, 1.24, _ ],[
    'Flex',   5.07, 4.05, 3.04, 2.03, 1.01, _ ],[
    'Resl',   7.07, 5.65, 4.24, 2.83, 1.41, _ ],[
    'Pmat',   7.80, 6.24, 4.68, 3.12, 1.56, _ ],[
    'Team',   5.48, 4.38, 3.29, 2.19, 1.01, _ ]],
    weighFeature = weighFeature,
    _split = split,
    _isCocomo = False
    )

def _kemerer(): print(kemerer())