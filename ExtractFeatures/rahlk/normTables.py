"""
Read an input table, which would be in a .csv format, 
normalize the numerical rows and leave the symbolic rows intact. 
"""
from __future__ import division
from table import *
import sys
sys.dont_write_bytecode = True
lo=2*[None]; hi=2*[None];
source='data/nasa93.csv'

def say(x): 
    sys.stdout.write(str(x))
    sys.stdout.flush()

values=[];

def what2show(keys):
    return [k for k in sorted(keys) if not "_" == str(k)[0]]
"""
def minmax(val):
    indx=0;
    for i in val:
        if(not isa(i,str)): 
            if(lo[indx]==None or lo[indx]>i):
                lo[indx]=i;
            if(hi[indx]==None or hi[indx]<i):
                hi[indx]=i;
            indx+=1
    return hi, lo

def normalizit(val,high,low):
    indx=0;
    for i in xrange(len(val)):
        if(not isa(val[i],str)):
            val[i]=(val[i]-low[indx])/(high[indx]-low[indx]);
            indx+=1
    return val
"""

t0=table(source)

rows = map(lambda x :x.cells,t0._rows)

#______________________________________________________________________________
for x in t0._rows:
    # Obtain the dictionary values of each row
    y=x.__dict__
    # Obtain the keys and values of a dictionary
    values=y['cells'] 
    #Max, Min= minmax(values)
    #print values
    #print Max, Min
#______________________________________________________________________________

t1=clone(t0);
## ** Put the above statements in the minmax function **
#print Max, Min
for x in t0._rows:    # Obtain the dictionary values of each row
    y=x.__dict__
    # Obtain the keys and values of a dictionary
    values=y['cells'] 
#    print normalizit(values,Max,Min)    
    
        