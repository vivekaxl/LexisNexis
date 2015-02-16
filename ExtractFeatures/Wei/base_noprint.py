from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True

rand= random.random


class Options: #"Thanks for Peter Norvig's trick"
  def __init__(i, **d): i.__dict__.update(d)

Settings = Options(sa = Options(kmax = 1000, 
	                              baseline = 1000,
                                score = {},
                                cooling = 0.5),
                   mws = Options(threshold = 0.0001,
                                max_tries = 20, 
                                max_changes = 1000,
                                prob = 0.25,
                                score = {}
                                ), 
                   other = Options(keep = 128, 
                                   era = 50,
                                   lives = 3,
                                   a12 = [0.56, 0.64, 0.71][0],
                                   repeats = 30))
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
    # print "\n" +("-"*60)
    # dump(Settings, f.__name__)
    # print "\n# Runtime: %.3f secs" % (endTime-beginTime)
    return x # return the searcher name and the results
  return wrapper

def dump(d, searchname, lvl = 0): # tricks from Dr. Menzies
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
    if k == searchname or k == "other":
      print gap + (" :{0} {1}".format(k, "options"))
      dump(d[k], lvl+1)

