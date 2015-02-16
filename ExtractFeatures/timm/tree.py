import re,math
log=math.log

def golf(): return """
   outlook, $temp,$humidity,wind,play
   overcast, 83, 86, false, yes
   overcast, 64, 65, true, yes
   overcast, 72, 90, true, yes
   overcast, 81, 75, false, yes
   rainy, 70, 96, false, yes
   rainy, 68, 80, false, yes
   rainy, 65, 70, true, no
   rainy, 75, 80, false, yes
   rainy, 71, 91, true, no
   sunny, 85, 85, false, no
   sunny, 80, 90, true, no
   sunny, 72, 95, false, no
   sunny, 69, 70, false, yes
   sunny, 75, 70, true, yes
   """

def showd(d):
  """Catch key values to string, sorted on keys. 
     Ignore hard to read items (marked with '_')."""
  name=''
  if not isinstance(d,dict):
    name = d.__class__.__name__
    d    = d.__dict__
  return name + '{'+ ' '.join([':%s %s' % (k,v)
            for k,v in sorted(d.items())
            if not "_" in k]) + '}'

class Counts():
  def __init__(i,inits=[]):
    i.n = 0.0
    i.cache = {}
    for x in inits:  i + x
  def __add__(i,x) :
    i.n += 1
    i.cache[x] = i.cache.get(x,0) + 1
  def __sub__(i,x) : 
    i.n -= 1
    i.cache[x] = i.cache.get(x,0) - 1
  def ent(i):
    e = 0
    for x in i.cache:
      p  = i.cache[x]*1.0/i.n
      if p:
        e -= p*log(p)/log(2)
    return e

class Bag():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i.id = Bag.id = Bag.id + 1
  def also(i,**d)   : i.override(d) 
  def override(i,d) : i.__dict__.update(d)
  def __repr__(i)   : return showd(i)

class Col(object):
  def __init__(i,name,pos):
    i.name, i.pos = name,pos
  def __repr__(i) : return showd(i)

class Num(Col):
  def __init__(i,name,pos):
    super(Num,i).__init__(name,pos)
    i._at = []
  def seen(i,x,at):
    i._at += [(x,at)]
    
class Sym(Col):
  def __init__(i,name,pos):
    super(Sym,i).__init__(name,pos)
    i._where, i.counts = {}, Counts()
  def seen(i,x,at) : 
    i.counts[x] += 1; 
    if x in i._where: 
      i._where[x] += [at]
    else:
      i._where[x] = [at]
    return x

def atoms(str,sep=',', bad=r'(["\' \t\r\n]|#.*)'):
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError: return x 
  str = re.sub(bad,"",str)
  if str:
    return map(atom,str.split(sep))
  
def rows(f): 
  for line in f().splitlines():
    row = atoms(line)
    if row:
      yield row

def newTable(cells):
  def what(txt,j): 
    klass = Num if '$' in txt else Sym
    return klass(txt,j)
  def nump(x):
    return isinstance(x,Num)
  t = Bag(_rows = [],
          cols = [what(txt,pos) for pos,txt
                  in enumerate(cells)])
  t.dep   = t.cols[-1]
  t.indep = t.cols[:-1]
  t.nums  = [c for c in t.indep if nump(c)]
  return t

def newRow(t,cells):
  row = Bag(of = t)
  row.cells = [col.seen(cells[col.pos],row) 
               for col in t.cols] 
  t._rows += [row]
  return t

def table(lst,t = None):
  for cells in lst:
    if t : newRow(t,cells)
    else : t = newTable(cells)
  return t

def nchops(t, num = lambda x: x[0],
              sym = lambda x: x[1].cells[0]):
  for col in t.nums:
    col.cuts = ediv(sorted(col._at),
                    (num,sym),
                    [])

 
