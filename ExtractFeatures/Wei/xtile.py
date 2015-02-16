from __future__ import division
import sys, random, math, datetime, time,re,pdb
sys.dont_write_bytecode = True


def pairs(lst):
  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i

def xtile(lst,lo=0,hi=0.0001, width = 50, 
             chops=[0.1 ,0.3,0.5,0.7,0.9],
             marks=["-" ," "," ","-"," "],
             bar="|",star="*",show="%3s"):
  """The function _xtile_ takes a list of (possibly)
  unsorted numbers and presents them as a horizontal
  xtile chart (in ascii format). The default is a 
  contracted _quintile_ that shows the 
  10,30,50,70,90 breaks in the data (but this can be 
  changed- see the optional flags of the function).
  """
  # ordered_list = sorted(lst)  # Dr.Menzies tricks
  # lo = min(lo, ordered_list[0])
  # hi = max(hi, ordered_list[-1])
  # showNumbers = [ ordered_list[int(percent * len(lst))] for percent in chops]
  # # print showNumbers
  # showMarks = [" "] * width
  # def find_index (x):
  #   return int(width*float((x-lo))/(hi-lo))
  # markIndex = [find_index(i) for i in showNumbers]
  # for i in range(width):
  #   if i in range(markIndex[0],markIndex[1]+1) or i in range(markIndex[-2],markIndex[-1]+1):
  #     showMarks[i] = "-"
  # #print showMarks  
  # showMarks[int(width * 0.5)] = "|"
  # showMarks[find_index(ordered_list[int(len(lst)*0.5)])] = "*"  
  # return " ".join(showMarks) + ", ".join([show %str(round(i,3)) for i in showNumbers])  
  def pos(p)   : return ordered[int(len(lst)*p)]
  def place(x) : 
    return int(width*float((x - lo))/(hi - lo+0.00001))
  def pretty(lst) : 
    return ', '.join([show % x for x in lst])
  ordered = sorted(lst)
  lo      = min(lo,ordered[0])
  hi      = max(hi,ordered[-1])
  what    = [pos(p)   for p in chops]
  where   = [place(n) for n in  what]
  out     = [" "] * width
  for one,two in pairs(where):
    for i in range(one,two): 
      out[i] = marks[0]
    marks = marks[1:]
  out[int(width/2)]    = bar
  out[place(pos(0.5))] = star 
  return ''.join(out) +  "," +  pretty(what)



def Demo() :
  import random
  random.seed(1)
  # nums = [random.random()**2 for _ in range(100)]
  #nums = [0.011,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
  nums = [0,0.1,0.1,0.6,0.4,0.1,0.9,0.1,0.1, 3]
  line = ' '*26+'='*23
  print ('%29s, %3s, %3s, %3s, %3s' % ('10%', '30%', '50%', '70%', '90%'))+'\n'+line
  print xtile(nums,lo=0,hi=1.0,width=25,)


if __name__ == "__main__": Demo()