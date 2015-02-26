from __future__ import division
import sys, random, math
from models import *
from base_noprint import *
import numpy as np
from xtile import *
sys.dont_write_bytecode = True


@printlook      
def sa(model):
  def P(old, new, t):
    prob = math.e**((old - new)/t) 
    return prob 
  min_energy, max_energy = model.baseline()
  s = model.generate_x()
  e = model.norm(model.getDepen(s))
  sb = s
  eb = e
  k = 1
  icontrol = Control(model)
  while k < Settings.sa.kmax:
    stopsign = icontrol.next(k) #true ---stop
    if stopsign:
      break
    sn = model.sa_neighbor(s)
    en = model.norm(model.getDepen(sn))
    icontrol.logxy(sn)
    temp = (k/Settings.sa.kmax)*Settings.sa.cooling
    if en < eb:
	  sb = sn
	  eb = en 
	  # say('!')
    if en < e:
      s = sn
      e = en
      # say('+')
    elif P(e, en, temp) < random.random():
      s = sn
      e = en
      # say('?')
    # say('.')
    k = k + 1
    # if k % 50 == 0:
      # print "\n"  
      # say(str(round(eb,3)))
  # print "\n"
  # printReport(model)
  # print "\n------\n:Normalized Sum of Objectives : ",str(round(eb,3)),"\n:Solution",sn
  lohi=printRange(model)
  return eb,lohi
#   
@printlook
def mws(model):

  min_energy, max_energy = model.baseline()
  total_changes = 0
  total_tries = 0
  norm_energy = 0
  eraScore = []
  control = Control(model)
  optimalsign = False
  solution = model.generate_x()
  norm_energy = model.norm(model.getDepen(solution))
  for k in range(Settings.mws.max_tries):
    total_tries += 1
    for _ in range(Settings.mws.max_changes):
      stopsign = control.next(total_changes) #true ---stop
      if stopsign:
        break
      if norm_energy <= Settings.mws.threshold:
        optimalsign = True
        break
      if  random.random()<=Settings.mws.prob:
        solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
        control.logxy(solution)
        # say("+")
      else:
        solution = model.mws_neighbor(solution)
        control.logxy(solution)
        # say("!")
      # say(".")
      # if total_changes % 50 == 0:
        # print "\n"
        # say(str(round(model.norm(model.getDepen(solution)), 3))) 
      total_changes +=1   
    if optimalsign or k == Settings.mws.max_tries-1:
      # say("\n")
      # say(str(round(model.norm(model.getDepen(solution)), 3))) 
      # print "\n"
      # print "total tries: %s" % total_tries
      # print "total changes: %s" % total_changes
      # print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
      # print "min_energy_obtained: %s" % model.getDepen(solution)
      # printReport(model)
      lohi =printRange(model)
      # print "\n------\n:Normalized Sum of Objectives: ",str(round(norm_energy,3)),"\n:Solution",solution, "\n"    
      return norm_energy, lohi


def printReport(m):
  for i, f in enumerate(m.log.y):
    print "\n <f%s" %i
    for era in sorted(m.history.keys()):
      # pdb.set_trace()
      log = m.history[era].log.y[i]
      print str(era).rjust(7), xtile(log._cache, width = 33, show = "%5.2f", lo = 0, hi = 1)

def printRange(m):
  lo = []
  lohi = []
  # print sorted(m.history.keys())
  for i, f in enumerate(m.log.y):
    tlo=10**5
    thi=-10**5
    for era in sorted(m.history.keys()):
      # pdb.set_trace()
      if m.history[era].log.y[i].lo < tlo:
        tlo= m.history[era].log.y[i].lo
      if m.history[era].log.y[i].hi > tlo:
        thi= m.history[era].log.y[i].hi
    lohi.append(tlo)
    lohi.append(thi)
  return  lohi
    # print "\n the range of f%s is %s to %s " % (i, str(tlo), str(thi))

@demo    
def start():
  r = Settings.other.repeats
  rlohi=[] # stupid codes here, to be fixed
  f1lo = []
  f1hi = []
  f0lo = []
  f0hi =[]
  f2lo =[]
  f2hi =[]
  # r = 2
  for klass in [Schaffer]:
  # for klass in [ZDT3, Viennet3]:
  #for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      name = klass.__name__
      n = 0.0
      reseed()
      scorelist = []
      for _ in range(r):
        x, lohi=searcher(klass())
      #========part 5==========
        rlohi.append(lohi)

      for i in range(0, r):
        f0lo.append(rlohi[i][0])
        f0hi.append(rlohi[i][1])
        f1lo.append(rlohi[i][2])
        f1hi.append(rlohi[i][3])
        if name == "Viennet3": # f1, f2, f3
          f2lo.append(rlohi[i][4])
          f2hi.append(rlohi[i][5])
      print "\n # The range of f0 during %s repeats is from %s to %s " \
             % (r, str(round(sorted(f0lo)[0], 3)), str( round(sorted(f0hi)[-1])))
      print "\n # The range of f1 during %s repeats is from %s to %s " \
             % (r, str(round(sorted(f1lo)[0],3)), str(round(sorted(f1hi)[-1])))
      if name =="Viennet3":
        print "\n # The range of f1 during %s repeats is from %s to %s "\
             % (r, str(round(sorted(f2lo)[0],3)), str(round(sorted(f2hi)[-1])))
      rlohi = []
      f0hi = []
      f0l0 = []
      f1lo = []
      f1hi = []
      f2lo = []
      f2hi = []
      #=====part 5 ends===========

      #the following codes for hw3
      # n += float(x)
      # scorelist +=[float(x)]
      # print xtile(scorelist,lo=0, hi=1.0,width = 25)
      # print "# {0}:{1}".format(name, n/r)
@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










