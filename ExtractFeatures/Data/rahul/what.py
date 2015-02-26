"""

# A Better Where

WHAT uses an adaption of the WHERE2 strategy to implement a supervised
near-linear time top-down clustering algorithm.

+ At each division, it keeps a summary of the data in a new _centroid_ variable.
+ Instead of dividing the data in half at each division, WHAT
  splits in order to minimize the variance of the scores in each division. 



## Standard Header Stuff

"""
from __future__ import division,print_function
import  sys,random,math
sys.dont_write_bytecode = True
import sdiv

"""

# Support Code


# Place to store settings.

## Usual Header


## Anonymous Containers

"""
class o:
  id=0
  def __init__(i, **d): 
    i.id = o.id = o.id + 1
    i.has().update(**d)
  def has(i): return i.__dict__
  def update(i,**d) : i.has().update(d); return i
  def __repr__(i)   : 
    show=[':%s %s' % (k,i.has()[k]) 
          for k in sorted(i.has().keys() ) 
          if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show=map(lambda x: '\t'+x+'\n',show)
    return '{'+' '.join(show)+'}'

def defaults(**d):
  return o(_logo="""
                     <>
       .-"-"-.       ||______________________
      /=      \      ||-._`-._ :| |: _.-'_.-|
     |- /~~~\  |     ||   `-._`:| |:`_.-'   |
     |=( '.' ) |     ||-------`-' '-'-------|
     \__\_=_/__/     ||------_.-. .-._------|
      {_______}      ||  _.-'_.:| |:._`-._  |
    /` *       `'--._||-'_.-'  :| |:  `-._`-|
   /= .     [] .     { >~~~~~~~~~~~~~~~~~~~~~
  /  /|ooo     |`'--'||
 (   )\_______/      ||
  \``\/       \      ||
   `-| ==    \_|     ||
     /         |     ||
    |=   >\  __/     ||
    \   \ |- --|     ||
     \ __| \___/     ||
 jgs _{__} _{__}     ||
    (    )(    )     ||
 ^^~ `"-"  `"-"  ~^^^~^^~~~^^^~^^^~^^^~^^~^ """,
      what=o(minSize  = 4,    # min leaf size
             depthMin= 2,      # no pruning till this depth
             depthMax= 10,     # max tree depth
             prune   = True,   # pruning enabled?
             b4      = '|.. ', # indent string
             verbose = False,  # show trace info?
             goal    = lambda m,x : scores(m,x)
             ),
      seed    = 1,
      cache   = o(size=128)
  ).update(**d)


"""

## Simple, low-level stuff

"""
def oneTwo(lst):
  one = lst[0]
  for two in lst[1:]:
    yield one,two
    one = two
"""
### Maths Stuff

"""
def gt(x,y): return x > y
def lt(x,y): return x < y

def medianIQR(lst, ordered=False):
  if not ordered: 
    lst = sorted(lst)
  n = len(lst)
  q = n//4
  iqr = lst[q*3] - lst[q]
  if n % 2: 
    return lst[q*2],iqr
  else:
    p = max(0,q-1)
    return (lst[p] + lst[q]) * 0.5,iqr

def median(lst,ordered=False):
  return medianIQR(lst,ordered)[0]
"""

An accumulator for reporting on numbers.

"""
class N(): 
  "Add/delete counts of numbers."
  def __init__(i,inits=[]):
    i.zero()
    map(i.__iadd__,inits)
  def zero(i): 
    i.n = i.mu = i.m2 = 0
    i.cache= Cache()
  def sd(i)  : 
    if i.n < 2: 
      return 0
    else:       
      return (max(0,i.m2)/(i.n - 1))**0.5
  def __iadd__(i,x):
    i.cache += x
    i.n     += 1
    delta    = x - i.mu
    i.mu    += delta/(1.0*i.n)
    i.m2    += delta*(x - i.mu)
    return i
  def __isub__(i,x):
    i.cache = Cache()
    if i.n < 2: return i.zero()
    i.n  -= 1
    delta = x - i.mu
    i.mu -= delta/(1.0*i.n)
    i.m2 -= delta*(x - i.mu)  
    return i

class Cache:
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[]):
    i.all,i.n,i._has = [],0,None
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    i.n += 1
    if len(i.all) < The.cache.size: # if not full
      i._has = None
      i.all += [x]               # then add
    else: # otherwise, maybe replace an old item
      if random.random() <= The.cache.size/i.n:
        i._has = None
        i.all[int(random.random()*The.cache.size)] = x
    return i
  def has(i):
    if i._has == None:
      lst  = i.all = sorted(i.all)
      med,iqr = medianIQR(lst,ordered=True)
      i._has = o(
        median = med,      iqr = iqr,
        lo     = lst[0], hi  = lst[-1])
    return i._has
"""

### Random stuff.

"""
by   = lambda x: random.uniform(0,x) 
rseed = random.seed
any  = random.choice
rand = random.random

def seed(r=None):
  global The
  if The is None: The=defaults()
  if r is None: r = The.seed
  rseed(r)
"""

### List Handling Tricks

"""
def first(lst): return lst[0]
def second(lst): return lst[1]
def third(lst): return lst[2]
"""

### Printing Stuff

Print without newline:

"""
def say(*lst): 
  print(*lst,end="")
  sys.stdout.flush()
"""

Print a list of numbers without an excess of decimal places:

"""
def gs(lst) : return [g(x) for x in lst]
def g(x)    : 
  txt = '%g' % x
  return int(txt) if int(x) == x else float(txt)
"""

Pretty print a dictionary:

"""
def showd(d):
  def one(k,v):
    if isinstance(v,list):
      v = gs(v)
    if isinstance(v,float):
      return ":%s %g" % (k,v)
    return ":%s %s" % (k,v)
  return ' '.join([one(k,v) for k,v in
                    sorted(d.items())
                     if not "_" in k])
"""

## Decorator to run code at Start-up

"""
def go(f):
  "A decorator that runs code at load time."
  print("\n# ---|", f.__name__,"|-----------------")
  if f.__doc__: print("#", f.__doc__)
  f()
"""

## Handling command line options.

Convert command line to a function call.
e.g. if the file lib.py ends with

    if __name__ == '__main__':eval(todo())

then 

    python lib.py myfun :a 1 :b fred  

results in a call to  _myfun(a=1,b='fred')_.

"""
def todo(com="print(The._logo,'WHERE (2.0) you at?')"):
  import sys
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  def oneTwo(lst):
    while lst: yield lst.pop(0), lst.pop(0)
  def value(x):
    try:    return eval(x)
    except: return x
  def two(x,y): return x[1:] +"="+wrap(value(y))
  twos = [two(x,y) for x,y in oneTwo(sys.argv[2:])]
  return sys.argv[1]+'(**dict('+ ','.join(twos)+'))'
"""

## More interesting, low-level stuff

"""
def timing(f,repeats=10):
  "How long does 'f' take to run?"
  import time
  time1 = time.clock()
  for _ in range(repeats):
    f()
  return (time.clock() - time1)*1.0/repeats
"""

## Data Completion Tool

Fills in some details on a table of data. For example, 

     def nasa93():
       vl=1;l=2;n=3;h=4;vh=5;xh=6
       return data(indep= [ 
                     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
                     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
                     'ltex', 'tool', 'site', 'sced', 'kloc'],
                   less = ['effort', 'defects', 'months'],
                   _rows=[
                      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
                      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
                      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
     ...

Adds in information on _cols_, _decisions_, _hi,lo_, etc:

    {	:cols [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
             12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 
             22, 22, 23, 24]
 	    :decisions [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                  11, 12, 13, 14, 15, 16, 17, 18, 
                  19, 20, 21, 22]
 	    :eval <function <lambda> at 0x7f3f825bea28>
 	    :hi {0: 4, 1: 4, 2: 4, 3: 5, 4: 4, 5: 5, 6: 5, 
           7: 6, 8: 3, 9: 3, 10: 6, 11: 6, 12: 4, 13: 5, 
           14: 5, 15: 3, 16: 5, 17: 4, 18: 4, 19: 4, 
           20: 3, 21: 3, 22: 980, 23: 8211, 24: 50961}
 	    :lo {0: 4, 1: 4, 2: 4, 3: 5, 4: 2, 5: 2, 6: 2, 
           7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 2, 
           13: 3, 14: 3, 15: 3, 16: 2, 17: 1, 18: 1, 
            19: 3, 20: 3, 21: 2, 22: 0.9, 23: 8.4, 24: 28}
 	    :names ['Prec', 'Flex', 'Resl', 'Team', 'Pmat', 
              'rely', 'data', 'cplx', 'ruse', 'docu', 
              'time', 'stor', 'pvol', 'acap', 'pcap', 
              'pcon', 'aexp', 'plex', 'ltex', 'tool', 
              'site', 'sced', 'kloc', 'effort', 
              'defects', 'months']
 	    :objectives [22, 23, 24]
 	    :w {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 
          7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 
          14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 
          20: 1, 21: 1, 22: -1, 23: -1, 24: -1}
    }

Code:

"""
def row(lst):
  return o(cells=lst, score=0,
           scored=False, x0=None, y0=None) 

def data(indep=[], less=[], more=[], _rows=[]):
  nindep= len(indep)
  ndep  = len(less) + len(more)
  m= o(lo={}, hi={}, w={}, 
       eval  = lambda m,it : True,
       _rows = [row(r) for r in _rows],
       names = indep+less+more)
  m.decisions  = [x for x in range(nindep)]
  m.objectives = [nindep+ x- 1 for x in range(ndep)]
  m.cols       = m.decisions + m.objectives
  for x in m.decisions : 
    m.w[x]=  1
  for y,_ in enumerate(less) : 
    m.w[x+y]   = -1
  for z,_ in enumerate(more) : 
    m.w[x+y+z] =  1
  for x in m.cols:
    all = sorted(row.cells[x] for row in m._rows)
    m.lo[x] = all[0]
    m.hi[x] = all[-1]
  return m
"""

## Start-up Actions

## Dimensionality Reduction with Fastmp

Project data in N dimensions down to a single
dimension connecting twp distant points. Divide that
data at the median of those projects.

"""
def fastmap(m,data):
  "Divide data into two using distance to two distant items."
  one  = any(data)             # 1) pick anything
  west = furthest(m,one,data)  # 2) west is as far as you can go from anything
  east = furthest(m,west,data) # 3) east is as far as you can go from west
  c    = dist(m,west,east)
  # now find everyone's distance
  lst = []
  for one in data:
    a = dist(m,one,west)
    b = dist(m,one,east)
    x = (a*a + c*c - b*b)/(2*c) # cosine rule
    y = max(0, a**2 - x**2)**0.5 
    if one.x0 is None: one.x0 = x # for displaying
    if one.y0 is None: one.y0 = y # for displaying
    lst  += [(x,one)]
  lst = sorted(lst)
  splits = sdiv.divides(lst,
              tiny= 4,
              num1= first,
              num2= lambda z: scores(m,second(z)))
  return west,east, c, spreadOut(splits,f=second)

def spreadOut(lst, f=lambda z:z): 
  def oneTwo(lst):
    one = lst[0]
    for two in lst[1:]:
      yield one,two
      one = two
  out = [o(lo= cut1, hi= cut2, sd= sd1,
           data = map(f,data1))
         for (cut1,data1,sd1), (cut2,_,_) 
         in oneTwo(lst)]
  cut,data,sd = lst[-1]
  out += [o(lo=cut,hi=10**32,
            data = map(f,data), sd=sd)]
  out[0].lo = -10**32
  return out
"""

In the above:

+ _m_ is some model that generates candidate
  solutions that we wish to niche.
+ _(west,east)_ are not _the_ most distant points
  (that would require _N*N) distance
  calculations). But they are at least very distant
  to each other.

This code needs some helper functions. _Dist_ uses
the standard Euclidean measure. Note that you tune
what it uses to define the niches (decisions or
objectives) using the _what_ parameter:

"""
def dist(m,i,j,
         what = lambda m: m.decisions):
  "Euclidean distance 0 <= d <= 1 between decisions"
  n      = len(i.cells)
  deltas = 0
  for c in what(m):
    n1 = norm(m, c, i.cells[c])
    n2 = norm(m, c, j.cells[c])
    inc = (n1-n2)**2
    deltas += inc
    n += abs(m.w[c])
  return deltas**0.5 / n**0.5
"""

The _Dist_ function normalizes all the raw values zero to one.

"""
def norm(m,c,val) : 
  "Normalizes val in col c within model m 0..1"
  return (val- m.lo[c]) / (m.hi[c]- m.lo[c]+ 0.0001)
"""

Now we can define _furthest_:

"""
def furthest(m,i,all,
             init = 0,
             better = gt):
  "find which of all is furthest from 'i'"
  out,d= i,init
  for j in all:
    if i.id == j.id: continue
    tmp = dist(m,i,j)
    if better(tmp,d): 
      out,d = j,tmp
  return out
"""

And of course, _closest_:

"""
def closest(m,i,all):
  return furthest(m,i,all,init=10**32,better=lt)

def closestN(m,n,i,all):
  tmp = []
  for j in all:
    if i.id == j.id: continue
    d = dist(m,i,j)
    tmp += [ (d,j) ]
  return sorted(tmp)[-1*n:]
"""

### Model-specific Stuff

WHAT talks to models via the the following model-specific variables:

+ _m.cols_: list of indices in a list
+ _m.names_: a list of names for each column.
+ _m.decisions_: the subset of cols relating to decisions.
+ _m.obectives_: the subset of cols relating to objectives.
+ _m.eval(m,eg)_: function for computing variables from _eg_.
+ _m.lo[c]_ : the lowest value in column _c_.
+ _m.hi[c]_ : the highest value in column _c_.
+ _m.w[c]_: the weight for each column. Usually equal to one. 
  If an objective and if we are minimizing  that objective, then the weight is negative.


### Model-general stuff

Using the model-specific stuff, WHAT defines some
useful general functions.

"""
def some(m,x) :
  "with variable x of model m, pick one value at random" 
  return m.lo[x] + by(m.hi[x] - m.lo[x])

def scores(m,it):
  "Score an individual."
  if not it.scored:
    m.eval(m,it)
    new, w = 0, 0
    for c in m.objectives:
      val = it.cells[c]
      w  += abs(m.w[c])
      tmp = norm(m,c,val)
      if m.w[c] < 0: 
        tmp = 1 - tmp
      new += (tmp**2) 
    it.score = (new**0.5) / (w**0.5)
    it.scored = True
  return it.score
"""

## WHERE2 = Recursive Fastmap


WHERE2 finds everyone's else's distance from the poles
  and divide the data on the mean point of those
  distances.  This all stops if:

+  Any division has _tooFew_ solutions (say,
  less than _sqrt_ of the total number of
  solutions).
+ Something has gone horribly wrong and you are
  recursing _tooDeep_

This code is controlled by the options in [_The_ settings](settingspy).  For
example, if _The.pruning_ is true, we may ignore
some sub-tree (this process is discussed, later on).
Also, if _The.verbose_ is true, the _show_
function prints out a little tree showing the
progress (and to print indents in that tree, we use
the string _The.b4_).  For example, here's WHERE2
dividing 93 examples from NASA93.
 
    ---| _where |-----------------
    93
    |.. 46
    |.. |.. 23
    |.. |.. |.. 11
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 12
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 6.
    |.. |.. 23
    |.. |.. |.. 11
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 12
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 6.
    |.. 47
    |.. |.. 23
    |.. |.. |.. 11
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 12
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 6.
    |.. |.. 24
    |.. |.. |.. 12
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 12
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 6.


WHERE2 returns clusters, where each cluster contains
multiple solutions.

"""
def what(m,data):
  score = lambda x: The.what.goal(m,x)
  all   = N(map(score, data))
  return what1(m,data, sd=all.sd()) 
  
def what1(m, data, lvl=0, up=None, sd=None):
  node = o(val=None,_up=up,_kids=[], support=len(data),
           centroid= row(summary(data)),
           sd=sd, data=data)
  def tooDeep(): return lvl > The.what.depthMax
  def tooFew() : return len(data) < The.what.minSize
  def tooVaried(sdNew):
    if lvl   < The.what.depthMin: return False
    if sdNew >= sd: return True
    return False
  def show(suffix): 
    if The.what.verbose: 
      print(The.what.b4*lvl,len(data),
            suffix,' ; ',node.id,' :sd ',node.sd,sep='')
  if tooDeep() or tooFew():
    show(".")
  else:
    show("")
    west,east, c, splits = fastmap(m,data)
    node.update(c=c,east=east,west=west)
    for split in splits:
      if len(split.data) < len(data):
        if not tooVaried(split.sd):
            node._kids += [o(cut = (split.lo, split.hi),
                             sub = what1(m, split.data,
                                         lvl= lvl+1,
                                         up = node,
                                         sd = split.sd))]
  return node

def summary(rows):
  def med(*l): return median(l)
  rows = [x.cells for x in rows]
  return [med(*l) for l in zip(*rows)]
"""
## Tree Code

Tools for manipulating the tree returned by _what_.

### Primitive: Walk the nodes

"""
def nodes(tree,seen=None,steps=0):
  if seen is None: seen=[]
  if tree:
    i = id(tree)
    if not i in seen:
      seen += [i]
      yield tree,steps
      for kid in tree._kids:
        for sub,steps1 in nodes(kid.sub,seen,steps+1):
          yield sub,steps1

def centroids(tree):
  for node,_ in nodes(tree):
    yield node.centroid
"""

### Return nodes that are leaves

"""
def leaves(tree,seen=None,steps=0):
  for node,steps1 in nodes(tree,seen,steps):
    if not node._kids:
      yield node,steps1

def leaf(m,one,node):
  if node._kids:
    a = dist(m,one,node.west)
    b = dist(m,one,node.east)
    c = node.c
    x = (a*a + c*c - b*b)/(2*c) 
    #print(map(lambda x:x.cut,node._kids))
    for kid in node._kids:
      (lo, hi), sub = kid.cut, kid.sub
      if lo <= x < hi: return leaf(m,one,kid.sub)
  return node
"""

### Return nodes nearest to furthest

"""
def neighbors(leaf,seen=None,steps=-1):
  """Walk the tree from 'leaf' increasingly
     distant leaves. """
  if seen is None: seen=[]
  for down,steps1 in leaves(leaf,seen,steps+1):
    yield down,steps1
  if leaf:
    for up,steps1 in neighbors(leaf._up, seen,steps+1):
      yield up,steps1
"""

### Return nodes in Groups, Closest to Furthest


"""
def around(leaf, f=lambda x: x):
  tmp,last  = [], None
  for node,dist in neighbors(leaf):
    if dist > 0:
      if dist == last:
        tmp += [f(node)]
      else:
        if tmp:
          for one in tmp:
            yield last,one
        tmp   = [f(node)]
    last = dist
  if tmp:
    for one in tmp:
      yield last,one
"""

## Leave-one-out

"""

def loo(m):
  model = m()
  lst = model._rows
  for n,one in enumerate(lst):
    yield model,one, lst[:n] + lst[n+1:]
"""

## Data

"""
def nasa93():
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return data(indep= [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc'],
    less = ['effort'], #, 'defects', 'months'],
    _rows=[
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11.0],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21.0],
      [h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
      [h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28.0],
      [h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
      [h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21.0],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16.0],
      [h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
      [h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
      [h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
      [h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
      [h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12.0],
      [h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
      [h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
      [h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
      [h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
      [h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
      [h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
      [h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
      [h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
      [h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
      [h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
      [h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
      [h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
      [h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
      [h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
      [h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
      [h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
      [h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
      [h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
      [h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
      [h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
      [h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
      [h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
      [h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
      [h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
      [h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25.0],
      [h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
      [h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
      [h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
      [h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
      [h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
      [h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
      [h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
      [h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
      [h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
      [h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
      [h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
      [h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
      [h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
      [h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
      [h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
      [h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
      [h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
      [h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
      [h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
      [h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23.0],
      [h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
      [h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
      [h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
      [h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
      [h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
      [h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
      [h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
      [h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
      [h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  6.2, 12,477,15.4],
      [h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0],
    ])
"""

## NASA93

"""


"""

## Demo Code

### Code Showing the scores

"""
#@go
def _scores():
  m = nasa93()
  out = []
  for row in m._rows: 
    scores(m,row)
    out += [(row.score, [row.cells[c] for c in m.objectives])]
  for s,x in sorted(out):
    print(s,x)
"""

### Code Showing the Distances

"""
#@go
def _distances(m=None):
   if m == None:  m = nasa93
   m=m()
   seed(The.seed)
   for i in m._rows:
     j = closest(m,i,  m._rows)
     k = furthest(m,i, m._rows)
     idec = [i.cells[c] for c in m.decisions]
     jdec = [j.cells[c] for c in m.decisions]
     kdec = [k.cells[c] for c in m.decisions]
     print("\n",
           gs(idec), g(scores(m,i)),"\n",
           gs(jdec),"closest ", g(dist(m,i,j)),"\n",
           gs(kdec),"furthest", g(dist(m,i,k)))
"""

### A Demo for  What.

"""
def slope(m,test,train):
  tree   = what(m, train) 
  centers= [c for c in centroids(tree)]
  (d1,c1),(d2,c2) = closestN(m,2,test,centers)
  e1, e2 = c1.cells[-3], c2.cells[-3]
  w1,w2  = 1/d1, 1/d2
  ws     = w1 + w2
  return (e1*w1 + e2*w2) / ws

The=defaults()

@go
def _loo(m=nasa93):
  model= m()
  seed(1)
  global The
  The.what.update(verbose = False,
               minSize = len(model._rows)**0.5,
               prune   = False,
               depthMax= 10,
               depthMin= 1
               )
  def effort(row):
    return row.cells[-3]
  scores=dict(clusterk1=N(),k1=N())
  for score in scores.values():
    score.go=True
  for model,test,train in loo(m):
    say(".")
    want    = effort(test)
    tree    = what(model, train) 
    def clusterk1(score):
      nearby   =leaf(model,test,tree)
      nearest  = closest(model,test,nearby.data)
      got      = effort(nearest)
      score   += abs(want - got)/want
    def knn(score,k=1):
      some   = closestN(model,k,test,train)
      es     = sum(map(lambda x:effort(x[1]),some))
      got    = es/k
      score += abs(want - got)/want
    n = scores["clusterk1"]; n.go and clusterk1(n)
    n = scores["k1"];        n.go and knn(n)
  print("")
  for key,n in scores.items():
    if n.go:
      print(key,
            ":median",n.cache.has().median, 
            ":has",n.cache.has().iqr)
  exit()


def _what(m=nasa93):
  m= m()
  seed(1)
  global The
  print("L>",0.5*len(m._rows)**0.5)
  The.what.update(verbose = True,
               minSize = 0.5*len(m._rows)**0.5,
               prune   = False,
               depthMax= 10,
               depthMin= 0
               )
  tree = what(m, m._rows) 
  n=0
  print(sorted([node.id for node,_ in nodes(tree)]))
  for node,_ in leaves(tree):
    n += len(node.data)
    print(node.id, ' ',end='')
    for near,dist in neighbors(node):
      print(dist,near.id,' ',end='')
    print("")
  print("n>",n)
  filter = lambda z: z.id
  for node,_ in leaves(tree):
     print(filter(node), 
           sorted([x for x in around(node,filter)]))
  print("===================")
  #exit()
  failed=0
  for node1,_ in leaves(tree):
    for row in node1.data:
      node2  = leaf(m,row,tree)
      failed += (0 if node1.id == node2.id else 1)
  print("Failed:",failed)  
  centers=[c for c in centroids(tree)]
  n = N()
  for node1,_ in leaves(tree):
    for row in node1.data:
      got  = closest(m,row,centers).cells[-3]
      want = row.cells[-3]
      n   += abs(want - got)/want
  print(n.cache.has().median, n.cache.has().iqr)
#_what()

"""
93 ; 648 :sd 100000000000000000000000000000000
|.. 5. ; 688 :sd 0.131721985241
|.. 13 ; 832 :sd 0.0502816234631
|.. |.. 6. ; 48 :sd 0.0495902279838
|.. |.. 7. ; 336 :sd 0.0436064936524
|.. 6. ; 480 :sd 0.253591931506
|.. 15 ; 768 :sd 0.0510130486783
|.. |.. 7. ; 416 :sd 0.0340741425218
|.. 9. ; 912 :sd 0.0676309885992
|.. 19 ; 776 :sd 0.0242475250614
|.. |.. 6. ; 112 :sd 0.0154888423331
|.. |.. 5. ; 400 :sd 0.0044788943576
|.. |.. 8. ; 688 :sd 0.00248546657439
|.. 5. ; 352 :sd 0.146791230857
|.. 9. ; 48 :sd 0.0112509526784
|.. 6. ; 336 :sd 0.101468090104
|.. 6. ; 624 :sd 0.0276130175275
"""
