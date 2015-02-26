def nsplit(nums, tiny=3, what=lambda x:x):
  class tally:
    def __init__(i,inits=[]) : 
      i.s, i.n = 0.0, 0.0
      for x in inits: i+x
    def __add__(i,x) : i.s += x; i.n += 1
    def __sub__(i,x) : i.s -= x; i.n -= 1
    def mu(i)        : return i.s/i.n
    def copy(i): j=tally(); j.s,j.n=i.s,i.n; return j
  lst    = sorted(nums,key=what)
  lhs, all = tally(), tally(what(x) for x in lst)
  best, cut, rhs = 0, None, all.copy()
  for j,x in enumerate(lst):
    if  lhs.n > tiny and rhs.n > tiny:
      tmp= lhs.n/all.n * (lhs.mu() - all.mu())**2 + \
           rhs.n/all.n * (rhs.mu() - all.mu())**2
      if tmp > best:
        best,cut = tmp,j
    rhs - what(x)
    lhs + what(x)
  return lst[:cut],lst[cut:] if cut else lst

def _nsplit():
  import random
  r=random.random
  random.seed(0)
  print ""
  for x in nsplit([1,2,3,4,5,20,21,22,23,24]): print x
  print ""
  lst = []
  for _ in range(4):
    lst += [r()**2, r(), r()**0.2]
  for x in nsplit(lst): print x

_nsplit()

"""
# divide the numbers [1,2,3,4,5,10,21,22,23,24]
[1, 2, 3, 4, 5]
[20, 21, 22, 23, 24]

# divide 4 things near 0.25, 4 things near 0.5, and 4 things near 0.75 into two
[0.06703788358226874, 0.30331272607892745, 0.34033460395871157, 0.5112747213686085, 0.6143402281729003]
[0.7130482633329904, 0.7579544029403025, 0.8345971131976975, 0.8409457587440543, 0.8622441420148107, 0.8721765361010373, 0.9081128851953352]

"""
