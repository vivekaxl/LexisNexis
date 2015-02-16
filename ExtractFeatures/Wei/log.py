from __future__ import division
import sys, random, math,pdb
from base import * 
from a12 import *
sys.dont_write_bytecode = True


'''All these are based on Dr.Menzies' tricks and sample codes'''

class Log():
  def __init__(i, tolog = []):
    i._cache, i.n, i._report = [], 0, None
    i.setup()
    map(i.__iadd__, tolog)
  def __iadd__(i, tolog):
    if tolog == None: return tolog
    i.n += 1
    updated = False
    if len(i._cache) < Settings.other.keep:
      i._cache +=[tolog] 
      updated = True
    else:
      if rand() <= Settings.other.keep/i.n:
         i._cache[int(rand()*Settings.other.keep)] = tolog
         updated = True
    if updated:
      i._report = None
      i.updateLoHi(tolog)
    return i
  def has(i):
    if i._report == None:
      i._report = i.report()
    return i._report

class Num(Log):
  def setup(i):
    i.lo = 10**5
    i.hi = -10**5
  def updateLoHi(i,x):
    i.lo = min (i.lo, x)
    i.hi = max(i.hi, x)
  def median(i):
    n = len(i._cache)
    p = n//2
    if (n % 2) : return i._cache[p]
    q = p +1
    q = max(0, min(q,n))
    return (i._cache[p] + i._cache[q])/2
  def better(new,old):
    "better if (1)less median or (2)same and less iqr"
    t = Settings.other.a12
    betterIqr = new.has().iqr < old.has().iqr
    new.lessp = False
    if new.lessp:
      betterMed = new.has().median >= old.has().median
      same      = a12(old._cache, new._cache)  <= t
    else:
      betterMed = new.has().median <= old.has().median 
      same      = a12(new._cache, old._cache) <= t
    return betterMed, same, betterIqr
  def report(i):
    sortedCache = sorted(i._cache)
    n = len (sortedCache)
    return Options(
           median = i.median(),
           iqr = sortedCache[int(n*0.75)- int(n*0.5)],
           lo = i.lo,
           hi = i.hi)

@demo
def demoNum():
  for size in [16,32, 64,128, 256]:
    Settings.other.keep = size
    log = Num()
    for x in xrange(100000): log +=x
    print size, ":", log.has().median

if __name__ == "__main__": eval(cmd())
