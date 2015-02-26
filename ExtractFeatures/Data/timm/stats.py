import zipfile,re,os,fnmatch,copy,random

def values(str,  sep=",",
           bad= r'(["\' \t\r\n]|#.*)'):
  def value(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  return map(value,re.sub(bad,"",str).split(sep))

def gs(lst):
  return map(lambda x:eval('%g'%x), lst)

class DefaultDict(dict):
  def __init__(i, default=lambda:[]):
    i.default = default
  def __getitem__(i, key):
    if key in i: return i.get(key)
    return i.setdefault(key,i.default())

def interpolate(x, points):
  lo, hi = points[0], points[-1]
  x1, y1 = lo[0], lo[1]
  for x2,y2 in points[1:]:
    if x1 <= x <= x2:
      deltay = y2 - y1
      deltax = (x- x1)*1.0/(x2- x1)
      return y1 + deltay * deltax
    x1,y1 = x2,y2
  return hi[1]

def zippedFiles(zipped, pattern='*'):
  "Find files in a zip."
  with zipfile.ZipFile(zipped,'r') as archive:
    for file in archive.namelist():
      if fnmatch.fnmatch(file, pattern):
        lines = archive.open(file,'r')
        yield file, lines

def files(dir='.', pattern='*'):
  "Find files in a directory tree."
  for path, subdirs, files in os.walk(dir):
    for name in files:
      if fnmatch.fnmatch(name, pattern):
        file = path + '/' + name
        lines = open(os.path.join(path, name))
        yield file, lines

def namedCells(source, contents=files):
  "Return cells, with header info from line1."
  for file,lines in contents(source):
    print file
    names = None
    for line in lines:
      cells = values(line)
      if not names: 
        names = cells
      else: 
        yield file,zip(names,cells)

def ar(want,got)    : return want - got
def mar(want,got)   : return abs(ar(want,got))
def relerr(want,got): return (want-got)*1.0/want
def mre(want,got)   : return abs(relerr(want,got))
   
def wantgot(source,compare=ar, contents=files):
  "Return cells, compared to values in first col."
  for file,found in namedCells(source,contents):
    want = found[0][1]
    for what,got in found[1:]:
      yield file, what, compare(want,got)

def ttest(i,j,conf=95):
  return critical(i.n + j.n - 2,conf) < i.t(j)

class Nums():
  def __init__(i,some=[]):
    i.n = i.mu = i.m2 = i.s = 0.0; i.all=[]
    i.win = i.loss = i.tie = 0
    for x in some: i % x
  def __mod__(i,x):
    i.all += [x]
    i.n   += 1; 
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)
    if i.n > 1: i.s = 1.0*(i.m2/(i.n - 1))**0.5
  def __add__(i,j): return Nums(i.all + j.all)
  def t(i,j):
    signal = abs(i.mu - j.mu)*1.0
    noise  = (i.s**2/i.n + j.s**2/j.n)**0.5
    return signal / noise
  def __lt__(i,j):
    if i.win  > j.win : return True
    if i.win == j.win and i.loss < j.loss: 
      return True
    return False
  def winLoss(i,j,conf=95,reverse=False,same=ttest):
    if same(i,j,conf=conf):
      i.tie += 1; j.tie += 1
      return False # no one win or lost
    iBest= i.mu < j.mu if reverse else i.mu > j.mu
    if iBest:
      i.win += 1; j.loss+= 1
    else:
      i.loss+= 1; j.win += 1 
    return True # we have a winner

def critical(n, conf=95):
  return interpolate(n,
                     {95:((  1, 12.70 ), ( 3, 3.182),
                          (  5,  2.571), (10, 2.228),
                          ( 20,  2.086), (80, 1.99 ),
                          (320,  1.97 )),
                      99:((  1, 63.657), ( 3, 5.841),
                          (  5,  4.032), (10, 3.169),
                          ( 20,  2.845), (80, 2.64 ),
                          (320,  2.58 ))}[conf])

def bootstrap(y,z,conf=0.05,b=500):
  """The bootstrap hypothesis test from
     p220 to 223 of Efron's book 'An
    introduction to the bootstrap."""
  def testStatistic(y,z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    s1    = y.s 
    s2    = z.s 
    delta = z.mu - y.mu
    if s1+s2:
      delta =  delta/((s1/y.n + s2/z.n)**0.5)
    return delta
  def one(lst): return lst[ int(any(len(lst))) ]
  def any(n)  : return random.uniform(0,n)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0.0
  for i in range(b):
    if testStatistic(
      Nums([one(yhat) for _ in yhat]),
      Nums([one(zhat) for _ in zhat])) > tobs:
      bigger += 1
  return bigger / b >= conf

def _bootstrapd(): 
  random.seed(1)
  def worker(n=30,mu1=10,sigma1=1,mu2=10.2,sigma2=1):
    def g(mu,sigma) : return random.gauss(mu,sigma)
    x = [g(mu1,sigma1) for i in range(n)]
    y = [g(mu2,sigma2) for i in range(n)]
    return n,mu1,sigma1,mu2,sigma2,\
        'same' if bootstrap(Nums(x),Nums(y)) else 'different'
  print worker(30, 10.1,  1,  10.2, 1)
  print worker(30, 10.1,  1,  10.8, 1.4)
  print worker(30, 10.1,  10,  10.7, 1)
 
#real	112m49.771s
#user	109m36.048s
#sys	0m8.804s


#_bootstrapd()

#quit()

def _t():
  one = [105,112,96,124,103,92,97,108,105,110]
  two = [98,108,114,106,117,118,126,116,122,108]
  for want,fudge in [(True,1.0),  (True,1.1), 
                     (False,1.2), (False,9.0)]:
    t1  = Nums(two)
    t2  = Nums(map(lambda x:x*fudge, one))
    got = t1.winLoss(t2)
    print fudge,":testPassed",want == got,\
          "since :want",want,":got",got

def _demo(zipped='data/loo.zip'):  
  wme = DefaultDict(default=lambda :Nums())
  for file,rx,seen in wantgot(zipped,mre,zippedFiles):
    key = rx
    wme[key] % seen
  print ""
  for k1,v1 in wme.items():
    v1.name = k1
    print k1
    for k2,v2 in wme.items():
      if k1 > k2:
        print "\t",k2
        v1.winLoss(v2,reverse=True,same=bootstrap)
  for v in sorted(wme.values()):
    print '%3d %3d %3d %s' \
        % (v.win,v.tie,v.loss,v.name)

_demo()
