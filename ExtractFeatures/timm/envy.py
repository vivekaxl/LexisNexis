"""
#<
ENVY: near linear-time locality-based reasoning.
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved.

       __.....__        _..._ .----.     .----.               
   .-''         '.    .'     '.\    \   /    /.-.          .- 
  /     .-''"'-.  `. .   .-.   .'   '. /'   /  \ \        / / 
 /     /________\   \|  '   '  ||    |'    /    \ \      / /  
 |                  ||  |   |  ||    ||    |     \ \    / /   
 \    .-------------'|  |   |  |'.   `'   .'      \ \  / /    
  \    '-.____...---.|  |   |  | \        /        \ `  /     
   `.             .' |  |   |  |  \      /          \  /      
     `''-...... -'   |  |   |  |   '----'           / /       
                     |  |   |  |                |`-' /        
                     '--'   '--'                 '..'                                    
  
Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the following conditions are met:

1. Redistributions of source code must retain the
above copyright notice, this list of conditions and
the following disclaimer.

2. Redistributions in binary form must reproduce the
above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the
names of its contributors may be used to endorse or
promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###################################################
#>
                                     
# Standard Utilities

## Start up

"""

import sys,math,random,re
sys.dont_write_bytecode = True # disable writing .pyc files

## Synonyms todo
seed = random.seed     # convenient shorthand
any  = random.choice   # another convenient shorthand

## Pretty Print

### Print, no New Line
def say(x):
  "Output a string, no trailing new line."
  sys.stdout.write(x)

### Print a Dictionary
def showd(d):
  """Catch key values to string, sorted on keys.
     Ignore hard to read items (marked with '_')."""
  d = d if  isinstance(d,dict) else d.__dict__
  return '{'+ ' '.join([':%s %s' % (k,v)
                        for k,v in
                        sorted(d.items())
                        if not "_" in k]) + '}'

### Print Nested Lists
def align(lsts,sep=' '):
  "Print, filled to max width of each column."
  widths = {}
  for lst in lsts: # pass1- find column max widths
    for n,x in enumerate(lst):
      w = len('%s' % x)
      widths[n] = max(widths.get(n,0),w)
  for lst in lsts: # pass2- print to max width
    for n,x in enumerate(lst):
      say(('%s' % x).rjust(widths[n],' ')+sep)
    print ""
  print ""

### Show Repeated Column Entries
def ditto(lst,old,mark="."):
  """Show 'mark' if an item of  lst is same as old.
     As a side-effect, update cache of 'old' values."""
  out = []
  for i,now in enumerate(lst):
    before = old.get(i,None) # get old it if exists
    out   += [mark if  before == now else now]
    old[i] = now # next time, 'now' is the 'old' value
  return out # the lst with ditto marks inserted

## Generic Slots
class Items():
  "Place to read/write/show named fields."
  def items(i) : return i.__dict__ 
  def override(i,d): i.items().update(d); return i
  def also(i, **d) : i.override(d)
  def __repr__(i) : 
    return showd(i.items())

class Slots(Items):
  "Items with a unique Id"
  id = -1
  def __init__(i,**d) : 
    i.id = Slots.id = Slots.id + 1
    i.override(d)
  def __eq__(i,j)  : return i.id == j.id   
  def __ne__(i,j)  : return i.id != j.id   

## Globals, Stored in 'The' Slots

The=Slots(reader = Slots(bad     = r'(["\' \t\r\n]|#.*)',
                         filter  = lambda x: atom(x),
                         keeping = '$=.<>!',
                         char    = Slots(sep=",",
                                         skip = '?')),
           nums = Slots(cache=128,
                        bins=5,
                        tiny=0.1, # dull= 60%-50% 
                        enough=10))

## Type Conversation
def atom(x):
  try              : return int(x)
  except ValueError:
    try              : return float(x)
    except ValueError: return x

def identity(X): return x

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def demo(f=None,demos=[]): 
  def demoDoc(d):
    return '# '+d.__doc__+"\n" if d.__doc__ else ""  
  if f == '-h':
    for d in demos: 
      print d.func_name+'()', demoDoc(d)
  if f: demos.append(f); return f
  s='|'+'='*40 +'\n'
  for d in demos: 
    print '\n==|',d.func_name,s,demoDoc(d),d()

## Iterators

### Nested List Iterator
def item(x) : 
  if isa(x,(tuple,list)):
    for y in x:
      for z in item(y): yield z
  else: yield x

### Tree Iterator
def nodes(t,lvl=0):
  "Iterator. Return all nodes."
  if t:
    yield lvl,t
    for t1 in [t._left,t._right]:
      for lvl1,leaf in nodes(t1,lvl+1):
        yield lvl1,leaf

### Leaf Iterator
def leafs(t):
  "Iterator: returns all leaf nodes."
  for lvl,node in nodes(t):
    if not node._left and not node._right:
      yield lvl,node

def tables(t0,tree):
  for _,leaf in leafs(tree):
    t1 = clone(t0)
    yield [body(row,t1) for row in leaf.value]

# Disk Tables

## CSV Reader
def rows(file, 
          sep   = The.reader.char.sep,
          bad   = The.reader.bad,
          filter= The.reader.filter):
  """Read comma-eperated rows that might be split 
  over many lines.  Finds strings that can compile 
  to nums.  Kills comments and white space."""
  n,kept = 0,""
  for line in open(file):
    now   = re.sub(bad,"",line)
    kept += now
    if kept:
      if not now[-1] == sep:
        yield n, map(filter,kept.split(sep))
        n += 1
        kept = "" 

## Skip "Ignored" Columns
def row(file,skip=The.reader.char.skip):
  "Leaps over any columns marked 'skip'."
  todo = None
  for n,line in rows(file):
    todo = todo or [col for col,name in enumerate(line) 
                    if not skip in name]
    yield n, [ line[col] for col in todo ]

## Read Headers and Rows
def table(source, rows = True, contents = row):
  t = table0(source)
  for n,cells in contents(source):  
    if n == 0 : head(cells,t) 
    else      : body(cells,t,rows) 
  return t

## Create Table 
def table0(source):
  t = Slots(source = source,
            depen=[], indep=[], nums =[], syms=[], 
            more =[], less =[], klass=[], headers=[], 
            _rows=[], at   ={})
  t.patterns= {'\$'    : t.nums,
               '\.'    : t.syms,
               '>'     : t.more,
               '<'     : t.less,
               '='     : t.klass,
               '[=<>]' : t.depen,
               '^[^=<>]': t.indep,
               '.'     : t.headers}
  return t

## Create Table Header
def head(cells,t,numc='$'):
  for col,cell in enumerate(cells):
    this   = Num if numc in cell else Sym
    header = this()
    header.col, header.name = col,cell
    t.at[cell] = header
    print ""
    for pattern,val in t.patterns.items():
      if re.search(pattern,cell):
        val += [header]
        print pattern,header,len(val)
      else:
        print "not",pattern, header.name
  #print "depen",t.depen
  print "indep",t.indep
  return t

## Create Table Rows
def body(cells,t,rows=True):
  for header in t.headers:
    header + cells[header.col]
  if rows: 
    t._rows += [cells]

def clone(t) :
  return head([h.name for h in t.headers],
              table0('copy of '+t.source))
  
# Meta Classes

## Sym
class Sym(Items):
  "An Accumulator for syms"
  def __init__(i): 
    i.n=i.most=0; i.mode= None; i.counts={}
  def __add__(i,x):
    i.n += 1    
    new  = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new, x
    i.counts[x] = new

## Num
class Num(Items):
  "An Accumulator for numbers"
  def __init__(i,init=[],
               cache=The.nums.cache,
               bins = The.nums.bins,
               tiny = The.nums.tiny): 
    i.n = i.m2 = i.mu = 0.0
    i.hi, i.lo = -1*10**32, 10**32
    i.some = Sample(cache=cache,bins=bins,tiny=tiny)
    for x in init: i + x
  def s(i) : return (i.m2/(i.n - 1))**0.5
  def __lt__(i,j): return i.mu < j.mu
  def __add__(i,x):
    i.some + x
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    i.n   += 1    
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)

## Sample
class Sample(Items):
  "Keep a random sample of stuff seen so far."
  def __init__(i,cache = 128, bins = 7, tiny=0.1):
    i._cache, i.size, i.n = [], cache, 0.0
    i.bins, i.tiny = bins, tiny
    i.stale()
  def stale(i)  : i._median,i._breaks = None,None
  def median(i) : i.fresh(); return i._median 
  def breaks(i) : i.fresh(); return i._breaks
  def fresh(i):
    if not i._median: 
      lst  = i._cache
      n    = len(lst)
      lst  = sorted(lst)
      p= q = int(n*0.5)
      r    = int(n*(0.5 + i.tiny))
      dull = lst[r] - lst[p]
      if n % 2: q = p + 1
      i._median = (lst[p] + lst[q])*0.5
      i._breaks = chops(lst, bins=i.bins,
                        sorted=True, dull=dull)
  def __add__(i,x):
    i.n += 1
    if len(i._cache) < i.size : # if cache not full
      i.stale()
      i._cache += [x]           # then add
    else: # otherwise, maybe replace an old item
      if random.random() <= i.size/i.n:
        i.stale()
        i._cache[int(random.random()*i.size)] = x

"""
def lohi(m,x):
  if m == nasa93:
    if   x==16: return 0,1000    # range of KLOC
    elif x==0 : return 1971,1987 # years
    else      : return 1,6 # 1..6 = vlow,low,nom,
                           #        hi,vhi,xhi
  else:
    raise Exception('[%s] unknown' % m.__name__)

def weight(m,x):
  if m == nasa93:
    return 1
  else:
    raise Exception('[%s] unknown' % m.__name__)

def project2Slots(project = nasa93()):
  "Returns 'Slots'- a struct with named fields."
  return [Slots( dec = col[:-1],
                 obj = [col[-1]
         ]) for col in project]

"""

# Discretization

def chops(lst,
          sorted= False,
          dull  = 0,
          bins  = 7,
          enough= The.nums.enough):
  def chop(bins, before, i):
    rest = len(lst) - i
    if rest < enough:
      return []
    inc = rest*1.0/bins
    j   = int(i + inc)
    while j < len(lst) and lst[j] <= before+dull:
      j += 1
    if j >= len(lst):
      return []
    now = lst[j]
    return [now] + chop(bins - 1, now,j)
  if not sorted:
    lst   = sorted(lst)
  now   = lst[0]
  return [now] + chop(bins, now,0)

# Glue

class Glue:
  def weight(i,x,focus) : pass
  def lohi(  i,x,focus) : pass
  def things(   i,x,focus) : pass
  def slots( i,x)            : pass

class Table(Glue):
  def __init__(i,file):
    i.t = table(file)
  def things(i,slots, focus=0):
    return slots.obj if focus else slots.dec
  def lohi(i,x, focus=0):
    what = i.t.depen if focus else i.t.indep
    h = what[x]
    return (h.lo, h.hi)
  def weight(i,x, focus=0): 
    return 1
  def slots(i):
    return [Slots( 
                dec= [row[h.col] for h in i.t.indep],
                obj= [row[h.col] for h in i.t.depen])
            for row in i.t._rows]
  def __repr__(i): return 'T' + showd(i)
  
# Distance Calculations

def dist(m,i,j,focus):
  "Euclidean distance 0 <= d <= 1 between things"
  thing1 = m.things(i,focus)
  thing2 = m.things(j,focus)
  #print len(thing1),len(thing2)
  deltas, n = 0, 0
  for d,x in enumerate(thing1):
    y = thing2[d]
    v1 = normalize(m,x,d,focus)
    v2 = normalize(m,y,d,focus)
    w  = m.weight(d)
    deltas,n = squaredDifference(m,v1,v2,w,deltas,n)
  return deltas**0.5 / (n+0.0001)**0.5

def normalize(m,x,d,focus):
  if not The.normalize : return x
  if x == The.missing  : return x
  if isinstance(x,str) : return x
  lo,hi = m.lohi(d,focus)
  return (x - lo)*1.0 / (hi - lo + 0.0001)
 
def squaredDifference(m,v1,v2,most,sum=0,n=0):
  def furthestFromV1() : 
    return  0 if v1 > 0.5 else 1
  inc = 0
  if not v1 ==  The.missing and not v2 == The.missing: 
    if v1 == The.missing: 
      v1,v2 = v2,v1 # at the very least, v1 is known
    if isinstance(v1,str) and isinstance(v2,str):
      if v2 == The.missing or v1 != v2 : 
        inc = 1
    else:
      if v2 == The.missing: v2 = furthestFromV1()  
      inc = (v1 - v2)**2
  return (sum + most*inc, # sum of incs, so far 
          n   + most) # sum of max incs, so far

# Clustering

def fastdiv(m,data,details, focus):
  "Divide data at median of two distant items."
  west, east = twoDistantPoints(m,data,focus)
  c    = dist(m, west, east, focus)
  for i in data:
    a   = dist(m,i, west, focus)
    b   = dist(m,i, east, focus)
    i.x = (a*a + c*c - b*b)/(2*c + 0.0001) # cosine rule
  data = sorted(data,key=lambda i: i.x)
  n    = len(data)/2
  details.also(west=west, east=east, c=c, cut=data[n].x)
  return data[:n], data[n:]

def twoDistantPoints(m,data,focus):
  def furthest(i):
    out,d= i,0
    for j in data:
      tmp = dist(m,i,j,focus)
      if tmp > d: out,d = j,tmp
    return out
  one  = any(data)      # 1) pick any thing
  west = furthest(one)  # 2) far from thing
  east = furthest(west) # 3) far from west
  return west,east

def settings(**has):
  "Return control settings for recursive descent."
  return Slots(minSize  = 10,    # min leaf size
               depthMin= 2,      # no pruning till depthMin
               depthMax= 10,     # max tree depth
               b4      = '|.. ', # indent string
               verbose = False,  # show trace info?
               focus   = 0      # cluster on indepent vars
   ).override(has)

def chunk(m,data,slots=None, lvl=0,up=None):
  "Return a tree of split data."
  slots = slots or settings()
  def tooFew() :
    return len(data) < slots.minSize
  def tooDeep():
    return lvl > slots.depthMax
  def show(suffix):
    if slots.verbose:
      print slots.b4*lvl + str(len(data)) + suffix
  tree= Slots(_up=up,value=None,_left=None,_right=None)
  if tooDeep() or tooFew():
    show(" #<-- %s" % tree.id)
    tree.value = data
  else:
    show("")
    wests,easts = fastdiv(m,data,tree,slots.focus)
    if not worse(wests, easts, tree) :
      tree._left = chunk(m,wests,slots,lvl+1,tree)
    if not worse(easts, wests, tree) :
      tree._right = chunk(m,easts,slots,lvl+1,tree)
  return tree

def worse(down1,down2,here): return False

def neighbors(m,this,tree,focus):
  def recurse(z):
    return neighbors(m, this, z, focus)
  left, right = tree._left, tree._right
  if not left and not right : return tree
  elif not right            : return recurse(left) 
  elif not left             : return recurse(right)
  else:
    a = dist(m, this, tree.west, focus)
    b = dist(m, this, tree.east, focus)
    c = tree.c
    x = (a*a + c*c - b*b)*1.0/(2*c + 0.0001) 
    return recurse(left if x < tree.cut else right)

def parents(tree):
  if tree:
    yield tree
    for up in parents(tree._up):
      yield up

def siblings(tree):
  visited = {tree.id: 1}
  for up in parents(tree._up):
    for _,down  in leafs(up):
      if not down.id in visited:
        visited[down.id] = 1
        yield down

# Demos

## Chops Demo
def _disc1():
  t= table("nasa93a.csv")
  for name,col in t.at.items():
    print "\n",name
    if isinstance(col,Sym):
      for key,count in col.counts.items():
        print "\t",key,count
    else:
      for key,x in enumerate(col.some.breaks()): 
        print "\t",key,x

## Chunk Demo
def _chunkDemo(model='nasa93'):
  seed(1)
  data   = project2Slots( model() )
  options= settings(verbose = True,
                    minSize = len(data)**0.5)
  tree   = chunk(model,  data ,options)
  eg,cid = 0,0
  for lvl,leaf in leafs(tree):
    context = leaf.value
    cid += 1
    print "----| cluster",cid,"|","-"*35
    lines  = []
    dittos = {}
    for row in sorted(context,key=lambda x:x.dec[0]):
      eg += 1
      pre = ["project ", eg,": "]
      params     = ditto(row.dec,dittos)
      params[0]  = str(params[0]) + " "
      params[-1] = " " + str(params[-1])
      lines     += [pre + params + [" = "] + row.obj]
    align(lines)

@demo
def _t1(f='data/nasa93a.csv'):
  "basic table "
  print f
  m = Table(f)
  tree = chunk(m,
               m.slots(),
               settings(verbose=True,minSize=6))
  id=0;
  for _,leaf in leafs(tree):
    id += 1
    print ""
    print leaf.id
    dittos={}
    #align([ditto(r.dec + r.obj,dittos) for r in leaf.value], sep=" , ")
    align([[id]+ r.dec + r.obj for r in leaf.value], sep=", ")

@demo
def _t2(f='data/nasa93nums.csv'):
  m      = Table(f)
  s      = m.slots()
  sets   = settings(verbose=True)
  tree   = chunk(m, s, sets)
  _,leaf = any([x for x in leafs(tree)])
  datum  = any([x for x in leaf.value])
  print leaf.id, datum.id
  print neighbors(m,datum,tree, sets.focus).id
  n=0
  for sib in siblings(leaf):
    n += 1
    print n,sib.id
  for t1 in tables(m.t,tree):
    print t1
    

The = Slots(normalize=True, missing='?')

if __name__ == '__main__': eval(cmd("_t1('data/weatherd.csv')"))

#print "obj:",map(lambda x: x.name, t.obj)
#print "dec:", map(lambda x: x.name, t.dec)

