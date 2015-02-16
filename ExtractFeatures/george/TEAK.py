from __future__ import division,print_function
import  sys  
sys.dont_write_bytecode = True
sys.path.extend(['/home/george/Panzer/Raise/Nasa 93'])
from lib import *
from where2 import *
from Models.nasa93 import *

# TODO implement TEAK
def teak(d=nasa93(), rows=None, verbose = False):
  rootNode = launchWhere2(d, rows, verbose)
  allLeaves = []
  for leaf, level in leaves(rootNode):
    allLeaves.append(leaf)
    
  for leaf in allLeaves:
    if ((leaf.variance > 1.25*leaf._up.variance) or (leaf.variance > 0.75*d.max_variance)):
      leaf._up._kids.remove(leaf)
  return rootNode
  
def leafTeak(m,one,node):
  if len(node._kids) > 1:
    east = node.east
    west = node.west
    mid_cos = node.mid_cos
    a = dist(m,one,west)
    b = dist(m,one,east)
    c = dist(m,west,east)
    x = (a*a + c*c - b*b)/(2*c)
    if (x<mid_cos):
      return leafTeak(m,one,node._kids[0])
    else:
      return leafTeak(m,one,node._kids[1])
  elif len(node._kids) == 1:
    return node._kids[0]
  return node

if __name__ == "__main__":
  teak()