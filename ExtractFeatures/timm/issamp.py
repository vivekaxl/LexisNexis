
def shuffle(lst):
  random.shuffle(lst)
  return lst

class Klash(Exception):
  def __init__(i, value):
    i.value = value
  def __str__(i):
    return str(i.value)

class Var:
  vars = {}
  def __init__(i,txt):
    Var.vars[txt] = None
    i.name = txt
  def __repr__(i):
    return '?%s' % i.name
  def __eq__(i,x):
    old = Var.vars.get(i.name,None)
    if isinstance(x,Var):
      return x == old
    if old != None and old != x:  
      raise Klash("%s[%s] is not %s" % (x,i,i.val))
    Var.vars[i.name] = x
    return True

a=Var("a")
a==1
a==1
try:
  a==2
except Klash as k:
  print k
  
def rands(*lst):
  tries = 5
  while True:
    tries -= 1
    try:
      yes = True
      for f in shuffle(lst): 
        if f() == False: 
          yes = False
          break
      if yes:
        return True 
    except Klash as k:
      if tries < 0: 
        raise k

def rors(*lst):
  tries = 5
  while True:
    tries -= 1
    try:
      yes = False
      for f in shuffle(lst): 
        if f():
          yes = True
          break
      if yes:
        return True
    except Klash as k:
      if tries < 0: 
        raise k
      



    
