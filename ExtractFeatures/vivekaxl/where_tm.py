'''
Created on Sep 18, 2014

@author: vivek
'''
"""

(Can be view as
[html](http://menzies.us/cs472/?niching) or [raw
Python](http://unbox.org/open/trunk/472/14/spring/src/where.py).)

How to Find Niche Solutions
===========================

### Why Niche?

When exploring complex multi-objective surfaces, it
is trite to summarize that space with one number
such _max distance from hell_ (where _hell_ is the
point in objective space where all goals have their
worse values). For example, all the following points
have the same _distance from hell_, but they reflect
very different solutions:
<center>
<img src="http://unbox.org/open/trunk/472/14/spring/doc/img/gunsbutter.png">
</center>

A better way to do it is _niching_; i.e. generate
the Pareto frontier, then cluster that frontier and
report a (small) number of random samples from each
cluster.  In this approach, "distance from hell" can
still be used internally to guide a quick search for
places to expand the frontier. But after that, we
can isolate interesting different parts of the
solution space.

For example, when exploring options for configuring
London Ambulances, Veerappa and Letier  use optimization to
reject thousands of options (shown in red) in order
to isolate clusters of better solutions C1,C2,etc
(shown in green). In this example, the goal is to
minimize X and maximize Y .
<center>
<img src="http://unbox.org/open/trunk/472/14/spring/doc/img/amus.png" width=400>
</center>

(REF: V. Veerappa and E. Letier, "Understanding
 clusters of optimal solutions in multi-objective
 decision problems, in RE' 2011, Trento, Italy,
 2011, pp. 89-98.)

### What is a Niche?

According to Deb and Goldberg (1989) _a niche is
viewed as an organism's task in the environment and
a species is a collection of organisms with similar
features_. 

+ REF: Kalyanmoy Deb and David
E. Goldberg. 1989.  [An Investigation of Niche and
Species Formation in Genetic Function
Optimization](http://goo.gl/oLIxo1). In
Proceedings of the 3rd International Conference on
Genetic Algorithms, J. David Schaffer (Ed.). Morgan
Kaufmann Publishers Inc., San Francisco, CA, USA,
42-50.

Their definition seems to suggest that niching means
clustering in objective space and species are the
things that form in each such cluster. Strange to
say, some of their examples report _niches_ using
decision space so all we can say is that it is an
engineering decision whether or not you _niche_ in
objective space or _niche_ in decision space. Note
that the above example from Veerappa and Letier
build niches in objective space while my code, shown
below, builds niches in decision space.

### How to Niche?

In any case, in decision or objective space, the
open issue is now to fun the niches? A naive
approach is to compute distances between all
individuals. This can be very slow, especially if
this calculation is called repeatedly deep inside
the inner-most loop of a program. In practice, any
program working with distance spends most of its
time computing those measures.  Various proposals
exist to prevent that happening:

+ _Canopy clustering_: McCallum, A.; Nigam, K.; and
   Ungar L.H. (2000) [ Efficient Clustering of High
   Dimensional Data Sets with Application to
   Reference Matching](http://goo.gl/xwIzN),
   Proceedings of the sixth ACM SIGKDD international
   conference on Knowledge discovery and data
   mining, 169-178 
+ _Incremental stochastic k-means_ [Web-Scale
  K-Means Clustering](http://goo.gl/V8BQs),
  WWW 2010, April 26-30, 2010, Raleigh, North
  Carolina, USA.
+ _Triangle inequality tricks_ (which work very well
  indeed) [Making k-means Even Faster](http://goo.gl/hk3Emn).
  G Hamerly - 2010 SIAM International Conference on
  Data Mining.

My own favorite trick is WHERE, shown below. It uses
a data mining trick to recursively divide the space
of decisions in two, then four, then eight,
etc. REF: [Local vs. global lessons for defect
prediction and effort
estimation](http://menzies.us/pdf/12gense.pdf) T
Menzies, A Butcher, D Cok, A Marcus, L Layman, F
Shull, B Turhan, IEEE Transactions on Software
Engineering 29 (6), 822-834, 2012.

WHERE uses a linear-time trick (called the FastMap
heuristic) to find two distant solutions- these are
the _poles_ called _west_ and _east_. Note that the
following takes only _O(2N)_ distance calculations:

"""
from numpy import *
from options import *

def fastmap(m,data):
  "Divide data into two using distance to two distant items."
  func1 = lambda a,b,c: (a*a + c*c - b*b)/(2*c)
  func2 = lambda a,b,c: (abs(a**2-((a*a + c*c - b*b)/(2*c))**2))**0.5

  one  = any(data)             # 1) pick anything
  west = furthest(m,one,data)  # 2) west is as far as you can go from anything
  east = furthest(m,west,data) # 3) east is as far as you can go from west
  c    = dist(m,west,east)
  # now find everyone's distance
  xsum,ysum = 0.0,0.0
  lst = []
  #file = open("test.txt","w+")
  for one in data:
    a = dist(m,one,west)
    b = dist(m,one,east)
    #try:
    x = func1(a,b,c)
    y = func2(a,b,c)
    #except:
    #    print 'continue'
    #    continue
    #x = (a*a + c*c - b*b)/(2*c) # cosine rule
    xsum += x
    ysum += y
    lst  += [(x,y,one)]
  # now cut data according to the mean distance
  cutx, wests, easts = xsum/len(data), [], []
  cuty, norths, souths = ysum/len(data), [], []
  #print "Length of the list: ",len(lst)
  for x,y,one in lst: 
    #print "Values >>>>>>>>>>",x,y,cutx,cuty
    if x < cutx and y < cuty: where = wests
    elif x > cutx and y < cuty: where = easts
    elif x < cutx and y > cuty: where = norths
    elif x > cutx and y > cuty: where = souths
    where += [one]
  return wests,easts,norths,souths
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
         what = lambda x: x.dec):
  "Euclidean distance 0 <= d <= 1 between decisions"
  d1,d2  = what(i), what(j)
  n      = len(d1)
  deltas = 0
  for d in range(n):
    n1 = norm(m, d, d1[d])
    n2 = norm(m, d, d2[d])
    inc = (n1-n2)**2
    deltas += inc
  return deltas**0.5 / n**0.5
"""

The _Dist_ function normalizes all the raw values zero to one.

"""
def norm(m,x,n) : 
  "Normalizes value n on variable x within model m 0..1"
  return (n - lo(m,x)) / (hi(m,x) - lo(m,x) + 0.0001)
"""

Now we can define _furthest_:

"""
def furthest(m,i,all,
             init = 0,
             better = lambda x,y: x>y):
  "find which of all is furthest from 'i'"
  out,d= i,init
  for j in all:
    if not i == j:
      tmp = dist(m,i,j)
      if better(tmp,d): out,d = j,tmp
  return out
"""

WHERE finds everyone's else's distance from the poles
  and divide the data on the mean point of those
  distances.  This all stops if:

+  Any division has _tooFew_ solutions (say,
  less than _sqrt_ of the total number of
  solutions).
+ Something has gone horribly wrong and you are
  recursing _tooDeep_

This code is controlled by a set of _slots_.  For
example, if _slots.pruning_ is true, we may ignore
some sub-tree (this process is discussed, later on).
Also, if _slots.verbose_ is true, the _show_
function prints out a little tree showing the
progress (and to print indents in that tree, we use
the string _slots.b4_).  For example, here's WHERE
dividing 100 solutions:
    
    100
    |.. 50
    |.. |.. 25
    |.. |.. |.. 11
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 5.
    |.. |.. |.. 14
    |.. |.. |.. |.. 6.
    |.. |.. |.. |.. 8.
    |.. |.. 25
    |.. |.. |.. 12
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 7.
    |.. |.. |.. 13
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 8.
    |.. 50
    |.. |.. 25
    |.. |.. |.. 13
    |.. |.. |.. |.. 7.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 12
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 7.
    |.. |.. 25
    |.. |.. |.. 11
    |.. |.. |.. |.. 5.
    |.. |.. |.. |.. 6.
    |.. |.. |.. 14
    |.. |.. |.. |.. 7.
    |.. |.. |.. |.. 7.

Here's the slots:

""" 
class Slots():
  "Place to read/write named slots."
  id = -1
  def __init__(i,**d) : 
    i.id = Slots.id = Slots.id + 1
    i.override(d)
  def override(i,d): i.__dict__.update(d); return i
  def __eq__(i,j)  : return i.id == j.id   
  def __ne__(i,j)  : return i.id != j.id   
  def __repr__(i)  : return '{' + showd(i.__dict__) + '}'

def where0(**other):
  return Slots(minSize  = 10,    # min leaf size
               depthMin= 2,      # no pruning till this depth
               depthMax= 3,     # max tree depth
               wriggle = 0.2,    # min difference of 'better'
               prune   = True,   # pruning enabled?
               b4      = '|.. ', # indent string
               verbose = True,  # show trace info?
               hedges  = 0.38    # strict=0.38,relax=0.17
   ).override(other)
"""

WHERE returns clusters, where each cluster contains
multiple solutions.

"""
def where(m,data,slots=where0()):
  out = []
  where1(m,data,slots,0,out)
  tempdata=[]
  for x in out:
    tempdata +=x
  
  return tempdata
mapping ={ 1:11,2:12,5:13,6:14,17:15,18:16,21:17,22:18,
           3:21,4:22,7:23,8:24,19:25,20:26,23:27,24:28,
           9:31,10:32,13:33,14:34,25:35,26:36,29:37,30:38,
           11:41,12:42,15:43,16:44,27:45,28:46,31:47,32:48,
           33:51,34:52,37:53,38:54,49:55,50:56,53:57,54:58,
           35:61,36:62,39:63,40:64,51:65,52:66,55:67,56:68,
           41:71,42:72,45:73,46:74,57:75,58:76,61:77,62:78,
           43:81,44:82,47:83,48:84,59:85,60:86,63:87,64:88
}

def where1(m, data, slots, lvl, out):
  def tooDeep(): return lvl >= slots.depthMax
  def tooFew() : return len(data) < slots.minSize
  def show(suffix): 
    if slots.verbose: 
      print slots.b4*lvl + str(len(data)) + suffix
  #print " >>>>>>>>>>>>>>>>>>>>>> %f %f"%(lvl,slots.depthMax)
  if tooDeep() or tooFew():
    #show(".")
    #print "++++++++++++++++++",slots.minSize
    #print "++++++++++++++++++",len(data)
    for x in data:
      x.num = len(out)+1
      #print mapping[x.num]
      x.xblock = mapping[x.num]/10
      x.yblock = mapping[x.num]%10
    #print " >>>>>>>>>>>>>>>>>>> %f "%(len(out)+1)
    #print data
    out += [data]
  else:
    #show("")
    #print "There", lvl
    wests,easts,norths,souths = fastmap(m,data) #wests: All the points to the left of the means, easts: All the points to the right of the means 
    #goLeft, goRight = maybePrune(m,slots,lvl,west,east) #goLeft,goRight is always True
    where1(m, wests, slots, lvl+1, out)
    where1(m, easts, slots, lvl+1, out)
    where1(m, norths, slots, lvl+1, out)
    where1(m, souths, slots, lvl+1, out)
"""

Is this useful? Well, in the following experiment, I
clustered 32, 64, 128, 256 individuals using WHERE or
a dumb greedy approach called GAC that (a) finds
everyone's closest neighbor; (b) combines each such
pair into a super-node; (c) then repeats
(recursively) for the super-nodes.

<center>
<img src="http://unbox.org/open/trunk/472/14/spring/doc/img/gacWHEREruntimes.png">
</center>



WHERE is _much_ faster than GAC since it builds
a tree of cluster of height log(N) by, at each
step, making only  O(2N) calls to FastMap.

### Experimental Extensions

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
def maybePrune(m,slots,lvl,west,east):
  "Usually, go left then right, unless dominated."
  goLeft, goRight = True,True # default
#   print "LLLLLLLLLLLLLLLLLLLLLLLLLLL",
#   print slots.prune
  if  slots.prune and lvl >= slots.depthMin:
    sw = scores(m, west)
    se = scores(m, east)
    if abs(sw - se) > slots.wriggle: # big enough to consider
      if se > sw: goLeft   = False   # no left
      if sw > se: goRight  = False   # no right
  return goLeft, goRight
"""

Note that I do not allow pruning until we have
descended at least _slots.depthMin_ into the tree.


Support Code
------------

### Dull, low-level stuff

"""
import sys,math,random
sys.dont_write_bytecode = True

def go(f):
  "A decorator that runs code at load time."
  print "\n# ---|", f.__name__,"|-----------------"
  if f.__doc__: print "#", f.__doc__
  f()

# random stuff
by   = lambda x: random.uniform(0,x) 
seed = random.seed
any  = random.choice

# pretty-prints for list
def gs(lst) : return [g(x) for x in lst]
def g(x)    : 
  if(x == None): return float(-1)
  return float('%g' % x) 
"""

### More interesting, low-level stuff

"""
def timing(f,repeats=10):
  "How long does 'f' take to run?"
  import time
  time1 = time.clock()
  for _ in range(repeats):
    f()
  return (time.clock() - time1)*1.0/repeats

def showd(d):
  "Pretty print a dictionary."
  def one(k,v):
    if isinstance(v,list):
      v = gs(v)
    if isinstance(v,float):
      return ":%s %g" % (k,v)
    return ":%s %s" % (k,v)
  return ' '.join([one(k,v) for k,v in
                    sorted(d.items())
                     if not "_" in k])

class Num:
  "An Accumulator for numbers"
  def __init__(i): i.n = i.m2 = i.mu = 0.0
  def s(i)       : return (i.m2/(i.n - 1))**0.5 #Standard Deviation
  def __add__(i,x):
    i.n   += 1    
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)

"""

### Model-specific Stuff

WHERE talks to models via the the following model-specific functions.
Here, we must invent some made-up model that builds
individuals with 4 decisions and 3 objectives.
In practice, you would **start** here to build hooks from WHERE into your model
(which is the **m** passed in to these functions).

"""
#def decisions() : return [0,1,2,3,4]
#def objectives(): return [0,1,2,3]
def lo(m,x)      : return m.minR[x]
def hi(m,x)      : return  m.maxR[x]
#def w(m,o)       : return 
def score(m, individual): #model
  if individual.changed == False: 
    return individual.scores
  temp = m.evaluate(individual.dec) 
  #print "Score| score: ",temp
  return temp
  


"""

The call to 
### Model-general stuff

Using the model-specific stuff, WHERE defines some
useful general functions.

"""
def some(m,x) :
  "with variable x of model m, pick one value at random" 
  return lo(m,x) + by(hi(m,x) - lo(m,x))

def candidate(m):
  "Return an unscored individual."
  return Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            num = -1,   #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

def scores(m,t):
  "Score an individual."
  if t.changed:
    t.scores = score(m,t)
    #print t.scores #Remove: just to be sure 
    t.changed = False
  return t.scores
  
  """
  Given a list. This function would return the median and the IQR
  """
def statisticList(list):
    if(len(list)!=0):
      print "Box Number: %d,%d"%(list[0].xblock,list[0].yblock),
      print " # of elements: %d"%len(list)
      for i in range(0,len(list[0].obj)):
        tmp=[]
        for j in range(0,len(list)):
            tmp.append(list[j].obj[i])
        print "Median of objective %d : %f,"%(i,median(tmp)),
        from scipy.stats import scoreatpercentile
        q1 = scoreatpercentile(tmp,25)
        q3 = scoreatpercentile(tmp,75)  
        print " IQR : %f"%(q3-q1)
      print
  
"""

### Demo stuff

To run these at load time, add _@go_ (uncommented) on the line before.

Checks that we can find lost and distant things:
@go
"""

def _distances():
  def closest(m,i,all):
    return furthest(m,i,all,10**32,lambda x,y: x < y)
  random.seed(1)
  m   = "any"
  pop = [candidate(m) for _ in range(4)]  
  for i in pop:
    j = closest(m,i,pop) #Find the closest point to i
    k = furthest(m,i,pop) #Find the farthest point to i
    print "\n",\
          gs(i.dec), g(scores(m,i)),"\n",\
          gs(j.dec),"closest ", g(dist(m,i,j)),"\n",\
          gs(k.dec),"furthest", g(dist(m,i,k))
    print i
"""

A standard call to WHERE, pruning disabled:
@go
"""

def whereMain2(model,points=[],depth=3):
  

  m, max, pop, kept = model,int(myoptions['Seive']['initialpoints']), [], Num()
  if len(points) == 0:
    for _ in range(max):
      one = candidate(m)  #Generate candidate
      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>^^^^^^^^^^^^^^^^^ %f"%one.xblock
      #kept + scores(m,one) #Store the scores in kept, mu: mean, m2: variance
      pop += [one]         #Store all the candidates in pop
  else:
    pop = points
    
  #print "Length of pop: ",len(pop)
  slots = where0(verbose = True,
               minSize = max**0.5,
               prune   = False,
               depthMax = depth) #removed wriggle
  #print "Deapth Max: ",slots.depthMax
  points = where(m, pop, slots)
  #print "Length of points: ",len(points)
  return points

"""

Compares WHERE to GAC:


@go
"""
def _whereTiming():
  def allPairs(data):
    n = 8.0/3*(len(data)**2 - 1) #numevals WHERE vs GAC
    for _ in range(int(n+0.5)):
      d1 = any(data)
      d2 = any(data)
      dist("M",d1,d2)
  random.seed(1)
  for max in [32,64,128,256]:
    m, pop, kept = "model",[], Num()
    for _ in range(max):
      one = candidate(m)
      kept + scores(m,one)
      pop += [one]

    slots = where0(verbose = False,
                minSize = 2, # emulate GAC
                depthMax=1000000,
                prune   = False,
                wriggle = 0.3*kept.s())
    t1 =  timing(lambda : where(m, pop, slots),10)
    t2 =  timing(lambda : allPairs(pop),10)
    print max,t1,t2, int(100*t2/t1)

def wheredemo(model,points=[],depth=3):
  #print "wheredemo"
  m, max, pop, kept = model,int(myoptions['Seive']['initialpoints']),[],Num()
  #print "Max: ",max
  if len(points) == 0:
    for _ in range(max):
      one = candidate(m)  #Generate candidate
      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>^^^^^^^^^^^^^^^^^ %f"%one.xblock
      #kept + scores(m,one) #Store the scores in kept, mu: mean, m2: variance
      pop += [one]         #Store all the candidates in pop
  else:
    pop = points
    
  #print "Length of pop: ",len(pop)
  slots = where0(verbose = True,
               minSize = 10,#,max**0.5,
               prune   = False) #removed wriggle
  #print "Deapth Max: ",slots.depthMax
  points = where(m, pop, slots)
  #print "Length of points: ",len(points)
  return points

#wheredemo()