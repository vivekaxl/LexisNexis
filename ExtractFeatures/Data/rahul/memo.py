# thing to determine kinds of cols

def  facet(f):
  key = f.__name__
  def theCache(obj):
    try:
      cache = obj.___cache
    except AttributeError:
      cache = obj.___cache = {}
    return cache
  def wrapper(obj): 
    cache= theCache(obj)
    if key in cache:
      return cache[key]
    else:
      tmp = cache[key] = f(obj)
      return tmp
  return wrapper


class Fred:
  @facet
  def n(i):
    print 1
    return len(i.__class__.__name__)

f = Fred()
print f.n()
print f.n()
