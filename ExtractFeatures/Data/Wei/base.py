from __future__ import division
import sys, random, math, datetime, time,re, pdb
from xtile import *
sys.dont_write_bytecode = True

rand= random.random


class Options: #"Thanks for Peter Norvig's trick"
  def __init__(i, **d): i.__dict__.update(d)

Settings = Options(sa = Options(kmax = 1000, 
                                cooling = 0.6),
                   mws = Options(threshold = 0.0001,
                                max_tries = 20, 
                                max_changes = 1000,
                                prob = 0.25,
                                ), 
                   ga = Options(pop = 50,
                                crossRate = 0.6,
                                crossPoints = 2,
                                genNum = [100, 200, 400, 800]
                                ),
                   de = Options(np= 100, 
                                repeats = 100, 
                                f = 0.75,
                                cr = 0.3,
                                threshold = 0.000001
                                ),
                   pso = Options(N = 30,
                                 w = 1,
                                 phi1 = 2.8,
                                 phi2 = 1.3,
                                 threshold = 0.000001,
                                 repeats = 1000,
                                ),
                   other = Options(keep = 64, 
                                   baseline = 1000,
                                   era = 50,
                                   lives = 1,
                                   show = False, 
                                   xtile = False,
                                   a12 = [0.56, 0.64, 0.71][0],
                                   repeats = 30,
                                   reportrange =False))
def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def demo(f=None,cache=[]):   
  def doc(d):
    return '# '+d.__doc__ if d.__doc__ else ""  
  if f == '-h':
    print '# sample demos'
    for n,d in enumerate(cache): 
      print '%3s) ' %(n+1),d.func_name,doc(d)
  elif f: 
    cache.append(f); 
  else:
    s='|'+'='*40 +'\n'
    for d in cache: 
      print '\n==|',d.func_name,s,doc(d),d()
  return f

def reseed():
	seed = 1
	return random.seed(seed)

def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()

def printlook(f):
  def wrapper(*lst): #tricks from Dr.Menzies
    ShowDate = datetime.datetime.now().strftime
    print "\n###", f.__name__, "#" * 50
    print "#", ShowDate("%Y-%m-%d %H:%M:%S")
    beginTime = time.time()
    x = f(*lst)
    endTime = time.time()
    print "\n" +("-"*60)
    dump(Settings, f.__name__)
    print "\n# Runtime: %.3f secs" % (endTime-beginTime)
    return x # return the searcher name and the results
  return wrapper

def dump(d, searchname=" ", lvl = 0): # tricks from Dr. Menzies
  d = d if isinstance(d, dict) else d.__dict__
  callableKey, line , gap = [], "", "  "*lvl
  for k in sorted(d.keys()):
    val= d[k]
    if isinstance(val, (dict, Options)):
      callableKey += [k]
    else:
      #if callable(val):
      #	val = val.__name__
      line +=("  {0} :{1}".format(k, val))
  print gap + line
  for k in callableKey:
    print gap + (" :{0} {1}".format(k, "options"))
    dump(d[k], lvl+1)

def printReport(m, history):
  for i, f in enumerate(m.log.y):
    print "\n <f%s" %i
    for era in sorted(history.keys()):
      # pdb.set_trace()
      log = history[era].log.y[i]
      print str(era).rjust(7), xtile(log._cache, width = 33, show = "%5.2f", lo = 0, hi = 1)


def printSumReport(m, history):
  # for i, f in enumerate(m.log.y):
  print "\n Objective Value" 
  for era in sorted(history.keys()):
    # pdb.set_trace()
    log = [history[era].log.y[k] for k in range (len(m.log.y))]
    ss = []
    ss.extend([log[s]._cache for s in range(len(log))])
    logsum = map(sum, zip(*ss))
    minvalue = min(logsum)
    maxvalue = max(logsum)
    normlog = [(x - minvalue)/(maxvalue - minvalue +0.00001) for x in logsum]
    print str(era).rjust(7), xtile(normlog, width = 33, show = "%5.2f", lo = 0, hi = 1)

def printRange(m, history):
  rrange = {}
  # print sorted(m.history.keys())
  for i, f in enumerate(m.log.y):
    tlo=10**5
    thi=-10**5
    for era in sorted(history.keys()):
      # pdb.set_trace()
      if history[era].log.y[i].lo < tlo:
        tlo= history[era].log.y[i].lo
      if history[era].log.y[i].hi > tlo:
        thi= history[era].log.y[i].hi
    temp = (round(tlo, 3), round(thi, 3))
    rrange[temp] =rrange.get(temp, 'f') +str(i) #{(0.0, 24.826): 'f0'}
  return  rrange
