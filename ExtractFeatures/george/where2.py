"""

# A Better Where

WHERE2 is a near-linear time top-down clustering alogithm.

WHERE2 updated an older where with new Python tricks.

## Standard Header Stuff

"""
from __future__ import division,print_function
import  sys  
sys.dont_write_bytecode = True
from lib import *
from Models import *
from numpy import var

MODEL =  nasa93.nasa93

"""

## Dimensionality Reduction with Fastmp

Project data in N dimensions down to a single dimension connecting
twp distant points. Divide that data at the median of those projects.

"""
def fastmap(m,data, what=lambda m: m.decisions):
  
  def centroid(lst):
    centroid = sum(lst)/len(lst)
    for i in range(len(lst)):
      if lst[i] > centroid:
        return centroid, i
    return centroid, len(lst)-1
  
  def sdiv(lst):
    bestVar = sys.maxint
    bestCut = len(lst)-1
    #for i in range(3,(len(lst) - 3)):
    for i in range(1,(len(lst) - 1)):
      lst_1, lst_2 = lst[:i],lst[i:]
      variance = (len(lst_1)*var(lst_1) + len(lst_2)*var(lst_2))/(len(lst_1)+len(lst_2))
      if variance < bestVar:
        bestVar, bestCut = variance, i
    return bestVar, bestCut
  
  "Divide data into two using distance to two distant items."
  one  = any(data)             # 1) pick anything
  west = furthest(m,one,data, what = what)  # 2) west is as far as you can go from anything
  east = furthest(m,west,data, what = what) # 3) east is as far as you can go from west
  c    = dist(m,west,east, what = what)
  # now find everyone's distance
  lst = []
  for one in data:
    a = dist(m,one,west, what = what)
    b = dist(m,one,east, what = what)
    if (c == 0):
      x = 0
    else :
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
    y = max(0, a**2 - x**2)**0.5 # not used, here for a demo
    lst  += [(x,one)]
  lst   = sorted(lst)
  if m._split == "variance":
    variance, mid = sdiv(map(first, lst))
  elif m._split == "centroid":
    centroid, mid = centroid(map(first,lst))
  else: #median
    mid   = len(lst)//2
  wests = map(second,lst[:mid])
  easts = map(second,lst[mid:])
  # Projection of midpoint, used for future testing
  mid_element = lst[mid]
  west = wests[0]
  east = easts[-1]
  return wests,west, easts,east,c, mid_element

 
"""
We select the leaf in which the test node
belongs by comparing the projection of
test node between the extreme nodes
"""
def leaf(m,one,node):
  if node._kids:
    east = node.east
    west = node.west
    mid_cos = node.mid_cos
    a = dist(m,one,west)
    b = dist(m,one,east)
    c = dist(m,west,east)
    if c == 0:
      return node
    x = (a*a + c*c - b*b)/(2*c)
    if (x<mid_cos):
      return leaf(m,one,node._kids[0])
    else:
      return leaf(m,one,node._kids[1])
  return node


"""
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
    if (hasattr(m,'weights') and len(m.weights)!=0) :
      inc = (m.weights[c] * (n1 - n2))**2
    else :
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
             better = gt,
						 what = lambda m:m.decisions):
  "find which of all is furthest from 'i'"
  out,d= i,init
  for j in all:
    if i == j: continue
    tmp = dist(m,i,j,what)
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
    if id(i) == id(j): continue
    d = dist(m,i,j)
    tmp += [ (d,j) ]
  return sorted(tmp)[:n]
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
def where2(m, data, lvl=0, up=None, verbose=True):
  node = o(val=None,_up=up,_kids=[])
  def tooDeep():
		return lvl > The.what.depthMax
  def tooFew() : return len(data) < m.minLeafSize
  def show(suffix): 
    if The.what.verbose: 
      print(The.what.b4*lvl,len(data),
            suffix,' ; ',id(node) % 1000,sep='')
  node.median_row = data[len(data)//2]
  node.variance = variance(m, data)
  if ((not hasattr(m, "max_variance")) or m.max_variance < node.variance):
    m.max_variance = node.variance
  node.val = data
  if tooDeep() or tooFew():
    if verbose:
      show(".")
  else:
    if verbose:
      show("")
    wests,west, easts,east,c, mid_element = fastmap(m,data)
    # TODO
    #if ((len(wests)<The.what.leafThreshold) or (len(easts)<The.what.leafThreshold)):
     # node._rows = wests + easts
      #print(len(node._rows))
    node.update(c=c,east=east,west=west,mid_cos=mid_element[0])
    goLeft, goRight = maybePrune(m,lvl,west,east)
    if goLeft: 
      node._kids += [where2(m, wests, lvl+1, node, verbose=verbose)]
    if goRight: 
      node._kids += [where2(m, easts,  lvl+1, node, verbose=verbose)]
  return node

"""

## An Experimental Extensions

Lately I've been experimenting with a system that
prunes as it divides the data. GALE checks for
domination between the poles and ignores data in
halves with a dominated pole. This means that for
_N_ solutions we only ever have to evaluate
_2*log(N)_ of them- which is useful if each
evaluation takes a long time.  

The niches found in this way
contain non-dominated poles; i.e. they are
approximations to the Pareto frontier.
Preliminary results show that this is a useful
approach but you should treat those results with a
grain of salt.

In any case, this code supports that pruning as an
optional extra (and is enabled using the
_slots.pruning_ flag). In summary, this code says if
the scores for the poles are more different that
_slots.wriggle_ and one pole has a better score than
the other, then ignore the other pole.

"""
def maybePrune(m,lvl,west,east):
  "Usually, go left then right, unless dominated."
  goLeft, goRight = True,True # default
  if  The.what.prune and lvl >= The.what.depthMin:
    sw = scores(m, west)
    se = scores(m, east)
    if abs(sw - se) > The.wriggle: # big enough to consider
      if se > sw: goLeft   = False   # no left
      if sw > se: goRight  = False   # no right
  return goLeft, goRight
"""

Note that I do not allow pruning until we have
descended at least _slots.depthMin_ into the tree.

### Model-specific Stuff

WHERE2 talks to models via the the following model-specific variables:

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

Using the model-specific stuff, WHERE2 defines some
useful general functions.

"""
def some(m,x) :
  "with variable x of model m, pick one value at random" 
  return m.lo[x] + by(m.hi[x] - m.lo[x])

def scores(m,it):
  "Score an individual."
  if not it.scored:
    #need for this line
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

def launchWhere2(m, rows=None, verbose=True, minSize = None):
  seed(1)
  told=N()
  if (not rows):
    rows = m._rows
  for r in rows:
    s =  scores(m,r)
    told += s
  global The
  The=defaults()
  The.what.update(verbose = True,
               #minSize = int(max(len(rows)**0.5,8)),
               #minSize = 4,
               minSize = int(len(rows)**0.5),
               prune   = False,
               wriggle = 0.3*told.sd(),
               leafThreshold = 4)
  if minSize :
    m.minLeafSize = minSize
  else :
    m.minLeafSize = The.what.minSize
  return where2(m, rows,verbose = verbose)

"""

## Tree Code

Tools for manipulating the tree returned by _where2_.
### Primitive: Walk the nodes

"""
def nodes(tree,seen=None,steps=0):
  if seen is None: seen=[]
  if tree:
   if not id(tree) in seen:
     seen.append(id(tree))
     yield tree,steps
     for kid in tree._kids:
       for sub,steps1 in nodes(kid,seen,steps+1):
         yield sub,steps1
"""

### Return nodes that are leaves

"""
def leaves(tree,seen=None,steps=0):
  for node,steps1 in nodes(tree,seen,steps):
    if not node._kids:
      yield node,steps1
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
          yield last,tmp
        tmp   = [f(node)]
    last = dist
  if tmp:
    yield last,tmp

    
"""

Compute variance of all rows

"""

def variance(m, rows):
  efforts = []
  for row in rows:
    efforts.append(effort(m, row))
  return var(efforts)
    
"""
## Demo Code

### Code Showing the scores

"""
#@go
def _scores():
  m = MODEL()
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
def _distances(m=MODEL):
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

### A Demo for  Where2.

"""
#@go
def _where(m=MODEL):
  m= m()
  seed(1)
  told=N()
  for r in m._rows:
    s =  scores(m,r)
    told += s
  global The
  The=defaults()
  The.what.update(verbose = True,
               #minSize = len(m._rows)**0.5,
               minSize = max(len(m._rows)**0.5,8),
               prune   = False,
               wriggle = 0.3*told.sd(),
               leafThreshold = 4)
  tree = where2(m, m._rows)
  
"""

## Start-up Actions

"""
if __name__ == '__main__': _where()