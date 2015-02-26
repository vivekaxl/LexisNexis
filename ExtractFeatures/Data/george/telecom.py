"""
# https://code.google.com/p/promisedata/source/browse/#svn%2Ftrunk%2Feffort%2Falbrecht

Standard header:

"""
from __future__ import division,print_function
import  sys
sys.dont_write_bytecode = True
from lib import *

"""
@attribute CHANGES numeric
@attribute FILES numeric
@attribute ACT_EFF numeric
"""

def telecom(weighFeature = False, 
           split = "variance"):
  vl=1;l=2;n=3;h=4;vh=5;xh=6;_=0
  return data(indep= [ 
     # 0..1
     'CHANGES','FILES'],
    less = ['ACT_EFF'],
    _rows=[
      [218,105,305.22],
      [357,237,330.29],
      [136,98,333.96],
      [25,24,150.4],
      [263,197,544.61],
      [39,39,117.87],
      [377,284,1115.54],
      [48,37,158.56],
      [118,53,573.71],
      [178,116,276.95],
      [59,38,97.45],
      [200,180,374.34],
      [53,43,168.12],
      [143,84,358.37],
      [257,257,123.1],
      [6,6,23.54],
      [5,5,34.25],
      [3,3,31.8]
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

def _telecom(): print(telecom())