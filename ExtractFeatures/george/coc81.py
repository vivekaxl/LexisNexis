"""
# The COC81 Data Set

Standard header:

"""
from __future__ import division,print_function
import  sys
sys.dont_write_bytecode = True
from  lib import *
"""

Data:

"""
def coc81(weighFeature = False,
          split = "variance"):
  vl=1;l=2;n=3;h=4;vh=5;xh=6;_=0
  return data(indep= [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc'],
    less = ['effort', 'defects', 'months'],
    _rows=[
      [h,h,h,vh,vl,l,vh,vl,n,n,n,h,h,l,l,n,l,l,n,vl,h,n,113,2040,13027,38.4],
      [h,h,h,vh,vl,l,vh,l,n,n,n,h,n,n,n,n,h,h,h,vl,h,n,293,1600,25229,48.6],
      [h,h,h,vh,n,n,vh,l,n,n,n,n,l,h,h,n,vh,h,h,l,h,n,132,243,3694,28.7],
      [h,h,h,vh,vl,vl,vh,vl,n,n,n,n,l,l,vl,n,h,n,h,vl,h,n,60,240,5688,28.0],
      [h,h,h,vh,vl,l,l,n,n,n,n,n,l,n,h,n,n,h,h,vl,h,n,16,33,970,14.3],
      [h,h,h,vh,vl,vl,n,l,n,n,n,vh,n,vl,vl,n,n,h,h,vl,h,n,4,43,553,11.6],
      [h,h,h,vh,n,vl,n,n,n,n,n,n,l,n,n,n,n,h,h,l,h,n,6.9,8,350,10.3],
      [h,h,h,vh,vl,h,l,vh,n,n,xh,xh,vh,vh,n,n,h,vl,vl,vl,h,l,22,1075,3511,24.5],
      [h,h,h,vh,n,h,l,vh,n,n,vh,vh,h,h,h,n,n,l,l,vl,h,n,30,423,1989,24.1],
      [h,h,h,vh,l,vh,l,vh,n,n,h,xh,n,h,h,n,vh,h,n,vl,h,n,29,321,1496,23.2],
      [h,h,h,vh,l,vh,l,vh,n,n,h,xh,n,h,h,n,vh,h,n,vl,h,n,32,218,1651,24.0],
      [h,h,h,vh,n,h,l,vh,n,n,h,h,n,h,h,n,vh,n,h,vl,h,l,37,201,1783,19.1],
      [h,h,h,vh,n,h,l,vh,n,n,h,h,h,vh,vh,n,n,l,n,vl,h,n,25,79,1138,18.4],
      [h,h,h,vh,vl,h,l,xh,n,n,vh,xh,h,h,vh,n,n,l,l,vl,h,vl,3,60,387,9.4],
      [h,h,h,vh,n,vh,l,vh,n,n,vh,h,h,h,h,n,l,vl,vl,vl,h,vl,3.9,61,276,9.5],
      [h,h,h,vh,l,vh,n,vh,n,n,vh,xh,n,h,h,n,n,n,n,vl,h,n,6.1,40,390,14.9],
      [h,h,h,vh,l,vh,n,vh,n,n,vh,xh,n,h,h,n,vh,n,n,vl,h,n,3.6,9,230,12.3],
      [h,h,h,vh,vl,h,vh,h,n,n,vh,vh,n,h,n,n,n,n,n,vl,h,l,320,11400,34588,52.4],
      [h,h,h,vh,n,h,h,n,n,n,h,vh,l,vh,n,n,h,n,n,l,h,n,1150,6600,41248,67.0],
      [h,h,h,vh,vl,vh,h,vh,n,n,h,vh,h,vh,n,n,vh,l,l,vl,h,l,299,6400,30955,53.4],
      [h,h,h,vh,n,n,vh,h,n,n,n,n,l,h,n,n,n,n,n,l,h,n,252,2455,11664,40.8],
      [h,h,h,vh,n,h,n,n,n,n,n,h,n,h,h,n,vh,h,n,vl,h,vl,118,724,5172,21.7],
      [h,h,h,vh,l,h,n,n,n,n,n,h,n,h,h,n,vh,h,n,vl,h,vl,77,539,4362,19.5],
      [h,h,h,vh,n,l,n,l,n,n,n,h,n,n,n,n,vl,l,h,n,h,n,90,453,4407,27.1],
      [h,h,h,vh,n,h,vh,vh,n,n,n,h,n,h,h,n,n,l,n,l,h,l,38,523,2269,20.2],
      [h,h,h,vh,n,n,n,l,n,n,n,h,h,h,h,n,n,l,n,vl,h,l,48,387,2419,18.5],
      [h,h,h,vh,n,h,l,h,n,n,n,vh,n,n,n,n,n,n,n,vl,h,l,9.4,88,517,12.1],
      [h,h,h,vh,vl,h,h,vh,n,n,h,vh,h,h,h,n,n,l,l,vl,h,n,13,98,1473,19.6],
      [h,h,h,vh,n,l,n,n,n,n,n,n,n,n,h,n,vl,n,n,l,h,vl,2.14,7.3,138,5.3],
      [h,h,h,vh,n,l,n,n,n,n,n,n,n,n,h,n,vl,n,n,l,h,vl,1.98,5.9,128,5.2],
      [h,h,h,vh,l,vh,h,n,n,n,n,xh,h,h,h,n,vh,l,l,vl,h,n,62,1063,3682,32.8],
      [h,h,h,vh,vl,l,h,l,n,n,n,n,n,vh,n,n,vh,n,n,vl,h,n,390,702,30484,45.8],
      [h,h,h,vh,n,vh,h,vh,n,n,n,xh,h,h,h,n,vh,h,n,l,h,n,42,605,1803,27.1],
      [h,h,h,vh,n,h,h,n,n,n,n,n,n,n,n,n,n,n,n,vl,h,vl,23,230,1271,14.2],
      [h,h,h,vh,vl,vl,l,vh,n,n,n,vh,h,n,n,n,h,l,n,vl,h,n,13,82,2250,17.2],
      [h,h,h,vh,l,l,n,n,n,n,n,n,l,l,l,n,n,h,h,l,h,n,15,55,1004,15.8],
      [h,h,h,vh,l,l,l,vl,n,n,n,h,n,h,h,n,vh,n,n,vl,h,n,60,47,2883,20.3],
      [h,h,h,vh,n,n,n,h,n,n,n,n,l,vh,n,n,h,h,h,l,h,n,15,12,504,13.5],
      [h,h,h,vh,n,n,n,h,n,n,n,n,l,vh,vh,n,vh,n,h,vl,h,n,6.2,8,197,9.6],
      [h,h,h,vh,vl,n,l,vh,n,n,n,n,n,h,l,n,vh,n,n,vl,h,n,n,8,294,9.5],
      [h,h,h,vh,n,l,l,n,n,n,n,n,l,n,vh,n,vh,h,h,l,h,n,5.3,6,173,8.7],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,h,n,n,n,h,h,vl,h,n,45.5,45,2645,21.0],
      [h,h,h,vh,l,n,n,n,n,n,n,vh,l,h,n,n,n,h,h,vl,h,n,28.6,83,1416,18.9],
      [h,h,h,vh,vl,l,n,n,n,n,n,vh,l,n,n,n,n,h,h,vl,h,n,30.6,87,2444,20.5],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,n,n,n,n,h,h,vl,h,n,35,106,2198,20.1],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,n,h,n,n,h,h,vl,h,n,73,126,4188,25.1],
      [h,h,h,vh,vl,vl,l,vh,n,n,n,n,l,vh,vh,n,vh,l,l,vl,h,n,23,36,2161,15.6],
      [h,h,h,vh,vl,l,l,l,n,n,n,n,l,l,l,n,h,h,h,vl,h,n,464,1272,32002,53.4],
      [h,h,h,vh,n,n,n,l,n,n,n,n,n,vh,vh,n,n,l,n,l,h,n,91,156,2874,22.6],
      [h,h,h,vh,l,h,n,n,n,n,vh,vh,n,h,h,n,n,l,n,vl,h,n,24,176,1541,20.3],
      [h,h,h,vh,vl,l,n,n,n,n,n,n,n,l,vl,n,n,n,h,vl,h,n,10,122,1225,16.2],
      [h,h,h,vh,vl,l,l,l,n,n,n,h,h,n,n,n,n,l,l,vl,h,n,8.2,41,855,13.1],
      [h,h,h,vh,l,l,l,h,n,n,h,vh,vh,vh,vh,n,n,l,l,vl,h,l,5.3,14,533,9.3],
      [h,h,h,vh,n,n,l,n,n,n,n,h,h,n,n,n,vh,n,h,vl,h,n,4.4,20,216,10.6],
      [h,h,h,vh,vl,l,l,vl,n,n,n,n,l,h,l,n,vh,h,h,vl,h,n,6.3,18,309,9.6],
      [h,h,h,vh,vl,h,l,vh,n,n,vh,vh,n,h,n,n,h,l,l,vl,h,l,27,958,3203,21.1],
      [h,h,h,vh,vl,n,l,h,n,n,h,vh,vh,n,n,n,n,l,l,vl,h,vl,17,237,2622,16.0],
      [h,h,h,vh,n,vh,l,vh,n,n,xh,vh,n,vh,vh,n,vh,h,h,vl,h,n,25,130,813,20.9],
      [h,h,h,vh,n,n,l,h,n,n,n,h,n,n,n,n,n,n,n,vl,h,n,23,70,1294,18.2],
      [h,h,h,vh,vl,h,l,vh,n,n,h,h,n,h,h,n,l,l,l,vl,h,l,6.7,57,650,11.3],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,n,h,n,vl,h,n,28,50,997,16.4],
      [h,h,h,vh,n,l,l,vh,n,n,h,vh,h,n,vh,n,vh,vl,vl,vl,h,n,9.1,38,918,15.3],
      [h,h,h,vh,n,n,l,h,n,n,n,n,n,vh,h,n,vh,n,n,vl,h,n,10,15,418,11.6]
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
    _split = split
    )
"""

Demo code:

"""
def _coc81(): print(coc81())

#if __name__ == '__main__': eval(todo('_nasa93()'))
