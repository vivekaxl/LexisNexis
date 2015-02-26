from __future__ import print_function
 
import sys
 
def test_function(*args, **kwargs):
  return 'args: ' + str(args) + '\nkwargs: ' + str(kwargs)

def a12():
  return 2

def say(*lst):
  print(*lst)
  return lst
 
def todo(do=['say', 'Anything you want.']):
  xs = sys.argv[1:] or do
  from itertools import takewhile, dropwhile
  #if not xs: return todo(do)
  def value(s):
    try: return eval(s)
    except: return s
  def is_kwargname(s):
    return s.startswith(':') if hasattr(s, 'startswith') else False
  isnt_kwargname = lambda s: not is_kwargname(s)
  f       = globals()[xs[0]]
  argable = map(value, xs[1:]) if xs[1:] else []
  args     = takewhile(isnt_kwargname, argable)
  kwargable = list(dropwhile(isnt_kwargname, argable))
  if not all(map(is_kwargname, kwargable[::2])):
    errstr = 'kwarg names should start with a colon (kwarg names: {})'
    ValueError(errstr.format(kwargable[::2]))
  else:
    mapping = zip(kwargable[::2], kwargable[1::2])
    kwargs = {k.strip(':'): value(v) for k, v in mapping}
    out = f(*args, **kwargs)
    if not out is None:
      print(out)

 
def f1(c,d,a=1,b=2):
  return c*d*(a+b)

if __name__ == '__main__':
  eval(todo())
