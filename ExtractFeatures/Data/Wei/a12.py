from __future__ import division
import  sys
sys.dont_write_bytecode = True
from base  import *

def _ab12():
  def a12slow(lst1,lst2):
    more = same = 0.0
    for x in sorted(lst1):
      for y in sorted(lst2):
        if   x==y : 
          same += 1
        elif x > y : 
          more += 1
    return (more + 0.5*same) / (len(lst1)*len(lst2))
  random.seed(1)
  l1 = [random.random() for x in range(5000)]
  more = [random.random()*2 for x in range(5000)]
  l2 = [random.random()  for x in range(5000)]
  less = [random.random()/2.0 for x in range(5000)]
  for tag, one,two in [("1less",l1,more), 
                       ("1more",more,less),("same",l1,l2)]:
    t1  = msecs(lambda : a12(l1,less))
    t2  = msecs(lambda : a12slow(l1,less))
    print "\n",tag,"\n",t1,a12(one,two)
    print t2, a12slow(one,two)

def a12(lst1,lst2):
  """how often is lst1 often more than y in lst2?
  assumes lst1 nums are meant to be greater than lst2"""
  def loop(t,t1,t2): 
    while t1.m < t1.n and t2.m < t2.n:
      h1 = t1.l[t1.m]
      h2 = t2.l[t2.m]
      h3 = t2.l[t2.m+1] if t2.m+1 < t2.n else None 
      if h1 > h2:
        t1.m  += 1; t1.gt += t2.n - t2.m
      elif h1 == h2:
        #if h3 and gt(h1,h3) < 0: original bugs
        if h3 and h1 > h3:
            t1.gt += t2.n - t2.m  - 1
        t1.m  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1,reverse=True)
  lst2 = sorted(lst2,reverse=True)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = Options(l=lst1,m=0,eq=0,gt=0,n=n1)
  t2   = Options(l=lst2,m=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)

if __name__ == "__main__": eval(cmd())
