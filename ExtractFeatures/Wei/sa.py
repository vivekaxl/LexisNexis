from __future__ import division
import sys, random, math
from models import *
from base import *
#this is a test
sys.dont_write_bytecode = True
# @printlook      
def sa(model):
  def P(old, new, t):
    prob = math.e**((old - new)/(t+0.00001)) 
    return prob 
  history = {}
  eb =0.0
  for _ in xrange(Settings.other.repeats):
    #reseed()
    min_energy, max_energy = model.baseline()
    s = model.generate_x()
    e = model.norm(model.getDepen(s))
    sb = s[:]
    eb = e
    k = 1
    icontrol = Control(model, history)
    while k < Settings.sa.kmax:
      stopsign = icontrol.next(k) #true ---stop
      if stopsign:
        break
      sn = model.sa_neighbor(s)
      en = model.norm(model.getDepen(sn))
      icontrol.logxy(sn)
      temp = (k/Settings.sa.kmax)**Settings.sa.cooling
      if en < eb:
        sb = sn[:] ###!!!!! can't do sb = sn for lists, because
        eb = en
        if Settings.other.show: say('!')
      if en < e:
        s = sn[:]
        e = en
        if Settings.other.show:say('+')
      elif P(e, en, temp) < random.random():
        s = sn[:]
        e = en
        if Settings.other.show:say('?')
      if Settings.other.show:say('.')
      k = k + 1
      if k % 30 == 0:
        if Settings.other.show:print "\n"  
        if Settings.other.show:say(str(round(eb,3)))
  if Settings.other.xtile: 
    printReport(model, history)
    print "\n"
    printSumReport(model, history)
  # print "\n------\n:Normalized Sum of Objectives : ",str(round(eb,3)),"\n:Solution",sb
  if Settings.other.reportrange:
    rrange=printRange(model, history)
    return eb,rrange
  else:
    return eb