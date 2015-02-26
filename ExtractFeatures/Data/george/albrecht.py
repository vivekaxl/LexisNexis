"""
# https://code.google.com/p/promisedata/source/browse/#svn%2Ftrunk%2Feffort%2Falbrecht

Standard header:

"""
from __future__ import division,print_function
import  sys
sys.dont_write_bytecode = True
from lib import *

"""
@attribute Input numeric
@attribute Output numeric
@attribute Inquiry numeric
@attribute File numeric
@attribute FPAdj numeric
@attribute RawFPcounts numeric
@attribute AdjFP numeric
@attribute Effort numeric
"""

def albrecht(weighFeature = False, 
           split = "variance"):
  vl=1;l=2;n=3;h=4;vh=5;xh=6;_=0
  return data(indep= [ 
     # 0..6
     'Input','Output','Inquiry','File','FPAdj','RawFPcounts','AdjFP'],
    less = ['Effort'],
    _rows=[
      [25,150,75,60,1,1750,1750,102.4],
      [193,98,70,36,1,1902,1902,105.2],
      [70,27,0,12,0.8,535,428,11.1],
      [40,60,20,12,1.15,660,759,21.1],
      [10,69,1,9,0.9,478.89,431,28.8],
      [13,19,0,23,0.75,377.33,283,10],
      [34,14,0,5,0.8,256.25,205,8],
      [17,17,15,5,1.1,262.73,289,4.9],
      [45,64,14,16,0.95,715.79,680,12.9],
      [40,60,20,15,1.15,690.43,794,19],
      [41,27,29,5,1.1,465.45,512,10.8],
      [33,17,8,5,0.75,298.67,224,2.9],
      [28,41,16,11,0.85,490.59,417,7.5],
      [43,40,20,35,0.85,802.35,682,12],
      [7,12,13,8,0.95,220,209,4.1],
      [28,38,24,9,1.05,487.62,512,15.8],
      [42,57,12,5,1.1,550.91,606,18.3],
      [27,20,24,6,1.1,363.64,400,8.9],
      [48,66,13,50,1.15,1073.91,1235,38.1],
      [69,112,21,39,1.2,1310,1572,61.2],
      [25,28,4,22,1.05,476.19,500,3.6],
      [61,68,0,11,1,694,694,11.8],
      [15,15,6,3,1.05,189.52,199,0.5],
      [12,15,0,15,0.95,273.68,260,6.1]
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

def _albrecht(): print(albrecht())