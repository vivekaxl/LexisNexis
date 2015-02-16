from __future__ import division
import sys, random, math
from sk import *
from sa import *
from mws import *
from ga import *
from de import *
from pso import *
from models import *
sys.dont_write_bytecode = True

@demo
def HW4part345(): #part 5 with part 3 and part4 
  for klass in [Schaffer,Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      reseed()
      x, rrange=searcher(klass()) #rrange is a dic: key is range, value is the obj name
      for key in rrange.keys():
        print "# The range of objective "+ str(rrange[key])+" during %s repeats is %s " \
             % (Settings.other.repeats, str(key))  
@demo
def HW4part6():
  def genvariants():
    Settings.sa.cooling = rand() # get variants of sa, mws
    Settings.mws.prob = rand()
    Settings.mws.max_changes = int(1000*rand())
  r = 20
  Settings.other.repeats = 1
  Settings.other.reportrange = False
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for variant in range(1):
      genvariants()
      allEB = []
      searcher = { "sa": sa, "mws" :mws}
      for key in searcher.keys():
        lastera = []
        reseed()
        for _ in range(r):
          model = klass()
          x = searcher[key](klass())
          lastera += [x]
        label = key + str(variant) 
        lastera.insert(0,label)
        allEB.append(lastera)
      rdivDemo(allEB) 
@demo 
def HW5():
  # for klass in [ Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3, DTLZ7]:
  for klass in [DTLZ7]:
    print "\n !!!!", klass.__name__
    allEB  = []
    searcher = {"sa":sa}
    #searcher = {"sa":sa, "mws":mws, "ga":ga}
    for key in searcher.keys():
      repeats = 5
      eb = 5*[0]
      name = klass.__name__
      reseed()
      for r in range(repeats):
        results=searcher[key](klass()) # lohi is a list containing [lo,hi] paris of f1&f2 
        if Settings.other.reportrange:
          eb[r] = results[0]
        else:
          eb[r] = results
      eb.insert(0, key)
      allEB.append(eb)
      rdivDemo(allEB)
@demo 
def HW6():
  for klass in [Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
  # for klass in [ Schaffer]:
    print "\n !!!!", klass.__name__
    allEB  = []
    #searcher = {"ga":ga}
    searcher = {"sa":sa, "mws":mws, "ga":ga, "de": de}
    Settings.other.repeats = 1
    for key in searcher.keys():
      repeats = 5
      eb = repeats*[0]
      name = klass.__name__
      reseed()
      for r in range(repeats):
        results=searcher[key](klass()) # lohi is a list containing [lo,hi] paris of f1&f2 
        eb[r] = results[0] if isinstance(results, tuple) else results
      eb.insert(0, key)
      allEB.append(eb)
      rdivDemo(allEB)
@demo 
def HW7():
  # for klass in [ Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3, DTLZ7,Schwefel, Osyczka]:
  for klass in [Osyczka]:
    print "\n !!!!", klass.__name__
    allEB  = []
    # searcher = {"sa":sa}
    searcher = {"sa":sa, "mws":mws, "ga":ga, "de": de, "pso":pso}
    Settings.other.repeats = 1
    for key in searcher.keys():
      repeats = 1
      eb = repeats*[0]
      name = klass.__name__
      reseed()
      ShowDate = datetime.datetime.now().strftime
     # print "#", ShowDate("%Y-%m-%d %H:%M:%S")
      beginTime = time.time()
      for r in range(repeats):
        results=searcher[key](klass()) # lohi is a list containing [lo,hi] paris of f1&f2 
        eb[r] = results[0] if isinstance(results, tuple) else results
      eb.insert(0, key)
      allEB.append(eb)
      endTime = time.time()
      # print "\n" +("-"*60)
      # dump(Settings, f.__name__)
      print "#"+key+" Runtime: %.3f secs" % (endTime-beginTime)
      # print "\n" +("-"*60)
    rdivDemo(allEB)
    dump(Settings,lvl = 0)

@demo
def testmodel():
  model = DTLZ7()
  # model = Osyczka()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










