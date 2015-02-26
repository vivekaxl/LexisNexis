from __future__ import division
import sys, random, math, pdb
from models import *
from base import *

def de(model):
  eb = 100.0
  np = Settings.de.np
  repeats = Settings.de.repeats
  fa = Settings.de.f
  cr = Settings.de.cr
  threshold = Settings.de.threshold
  min_e, max_e = model.baseline()
  # s = model.generate_x()
  # e = model.norm(model.getDepen(s))
  # sb = s[:]
  # eb = e
  indices = []
  scores = {}
  def evaluate(pop):
    for n, x in enumerate(pop):
      scores[n] = model.norm(model.getDepen(x))
    # print scores
    ordered = sorted(scores.items(), key=lambda x: x[1]) # alist of turple
    # print ordered
    return  pop[ordered[0][0]], ordered[0][1]
  def gen3(n,f,frontier):
    seen = [n]
    def gen1(seen):
      while 1:
        k = random.randint(0, np -1)
        if k not in seen:
          seen += [k]
          break
      return frontier[k]
    a = gen1(seen)
    b = gen1(seen)
    c = gen1(seen)
    return a, b, c

  def update(n,f,frontier):
    newf = []
    a, b, c = gen3(n,f,frontier)
    for n in xrange(len(f)):
      if cr <rand():
        newf.append(f[n])
      else:
        newf.append(model.trim(a[n]+fa*(b[n]-c[n]), n))  # adapt to the Osyzcka model, pass n
    return newf

  frontier = [model.generate_x() for _ in xrange(np)]
  sb, eb = evaluate(frontier)
  for k in xrange(repeats):
    if eb < threshold:
      break
    nextgen = []
    for n,f in enumerate (frontier):
      new = update(n, f, frontier)
      if model.norm(model.getDepen(new)) < model.norm(model.getDepen(f)):
        nextgen.append(new)
      else:
        nextgen.append(f)
    frontier = nextgen
    sb, eb = evaluate(frontier)
  #print eb
  if Settings.other.reportrange:
    rrange=printRange(model, history) # no history right now!
    return eb,rrange
  else:
    return eb

def deDemo():
  for klass in [Schaffer]:
  # for klass in [DTLZ7]:
    print "="*50
    print "!!!!", klass.__name__, 
    print "\nSearcher: DE"
    reseed()
    de(klass())
if __name__ == "__main__": deDemo()
  
