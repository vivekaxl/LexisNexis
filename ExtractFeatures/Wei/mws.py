from __future__ import division
import sys, random, math
from models import *
from base import *
sys.dont_write_bytecode = True
# @printlook
def mws(model):
  eraScore = []
  control = Control(model)
  optimalsign = False
  eb = 100.0
  norm_energy = 10**5
  history = {}
  for _ in xrange(Settings.other.repeats):
    min_energy, max_energy = model.baseline()
    control = Control(model, history)
    total_changes = 0
    total_tries = 0
    for k in xrange(Settings.mws.max_tries):
      if control.lives ==0:
        break
      solution = model.generate_x()
      total_tries += 1
      for _ in range(Settings.mws.max_changes):
        stopsign = control.next(total_changes) #true ---stop
        if stopsign:
          break
        norm_energy = model.norm(model.getDepen(solution))
        if norm_energy < Settings.mws.threshold:
          optimalsign = True
          break
        if  random.random()<Settings.mws.prob:
          solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
          control.logxy(solution)
          if Settings.other.show:say("+")
        else:
          solution = model.mws_neighbor(solution)
          control.logxy(solution)
          if Settings.other.show:say("!")
        if Settings.other.show:say(".")
        if total_changes % 30 == 0:
          if Settings.other.show:print "\n"
          if Settings.other.show:say(str(round(model.norm(model.getDepen(solution)), 3))) 
        total_changes +=1   
    # if optimalsign or k == Settings.mws.max_tries-1:
  if Settings.other.xtile: 
    say("\n")
    say(str(round(model.norm(model.getDepen(solution)), 3))) 
    print "\n"
    printReport(model, history)
    print "\n"
    printSumReport(model, history)
  if Settings.other.reportrange:
    rrange =printRange(model, history)
    return norm_energy, rrange
  else:
    return norm_energy