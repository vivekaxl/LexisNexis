from __future__ import division
from log import *
from models import *
from xtile import *
from base import *
import sys,random, math, pdb, operator
sys.dont_write_bytecode = True

# @printlook 
def pso(model):
  vel = []
  pos = []
  lbest = [] # local best position for each 
  gbest = model.generate_x() # global best position for all
  min_e, max_e = model.baseline()
  eb = 10**5
  N = Settings.pso.N
  w = Settings.pso.w
  repeats = Settings.pso.repeats
  threshold = Settings.pso.threshold
  phi1 = Settings.pso.phi1
  phi2 = Settings.pso.phi2
  phi = phi2 + phi1
  K = 2/(abs(2 - (phi) -math.sqrt(phi **2) -4*phi))
  fitness =lambda x: model.norm(model.getDepen(x)) 
  trim = lambda x : max(model.lo, min(x, model.hi)) 
  def init(gbest = gbest):
    for n in xrange(N):
      vel.append([0 for _ in xrange(model.n)])
      pos.extend([model.generate_x() for _ in xrange(model.n)])
      lbest.append(pos[n])
      if fitness(pos[n]) < fitness(gbest): #??why I should pass gbest
        gbest = pos[n]
        eb = fitness(gbest)
  def velocity(v, p, l, g):
    newVel = [K*(w*v[i]+phi1*rand()*(l[i]-p[i])+phi2*rand()*(g[i]-p[i])\
            )for i in xrange(model.n)]
    # print v 
    # print '\n'
    # print newVel
    return [model.trim(i,n) for n, i in enumerate(newVel)] # velosity should be in the range

  def move(v, p):
    newp = [v[i] + p[i] for i in xrange(model.n)]
    return [model.trim(i,n) for n, i in enumerate(newp)] # movements should be in the range


  init() # init all parameters
  # print vel
  # print lbest
  # print gbest
  for k in xrange(repeats):
    if eb < threshold:
      break
    for n in xrange(N):
      vel[n] = velocity(vel[n], pos[n], lbest[n], gbest)
      pos[n] = move(vel[n], pos[n])
      if fitness(pos[n]) < fitness(lbest[n]):
        lbest[n] = pos[n]
        if fitness(pos[n]) < fitness(gbest):
          gbest = pos[n]
    eb = fitness(gbest)
  return eb 
 
def start():
  # for klass in [Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
  for klass in [Kursawe, ZDT1, DTLZ7]: # these three can't find optimal values
    print "="*50
    print "!!!!", klass.__name__, 
    print "\nSearcher: PSO"
    reseed()
    pso(klass())

#test

if __name__ == "__main__":start()
     # print sortedFitness




    

