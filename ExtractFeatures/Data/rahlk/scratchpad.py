import numpy as np
r=[['a', 'a', 'a', 'b','c','c','c','c'],[1,2,3,13],[4,5,6,14],[7,8,9,15],[10,11,12,16,4,5,6,14]]

d={r[0][z]:[p[z] for p in r[1:] if z<=len(r[1])-1] for z in xrange(0,len(r[0]))}

def chardiv(lst):
    def pairs(xs):
      for p in zip(xs[:-1], xs[1:]): 
        yield p
    sortOrder=[i[0] for i in sorted(enumerate(lst[0]), key=lambda x:x[1], reverse=False)]
    sortedIndep=[i[1] for i in sorted(enumerate(lst[0]), key=lambda x:x[1], reverse=False)]
    sortedDep=[lst[1][z] for z in sortOrder]
    cuts=[];divs=[]
    for x in xrange(1,len(sortedIndep)):
      if not sortedIndep[x-1]==sortedIndep[x]:
        cuts.append(x)
    cuts.insert(0, 0); cuts.insert(len(cuts),len(sortOrder))
    for x,y in pairs(cuts):
      print x, y
      divs.append([sortedIndep[x],np.std(sortedDep[x:y]),[(sortedIndep[z], sortedDep[z]) for z in xrange(x,y)]])
    return divs

print chardiv([r[0],r[4]])