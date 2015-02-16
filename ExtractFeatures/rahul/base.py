import sys, os
sys.path.append(os.environ['HOME'] + '/git/axe/axe')
sys.path.insert(0, os.getcwd() + '/_imports');
from demos import *
from abcd import _runAbcd  # @UnresolvedImport
import sk;  # @UnresolvedImport
from dectree import *
from diffevol import *
from settings import *
from settingsWhere  import *
from pdb import set_trace

tree = treeings()
# set_trace()
def update(indep):
  whereParm = defaults().update(verbose = True,
                                minSize = int(indep[0]),
                                depthMin = int(indep[1]),
                                depthMax = int(indep[2]),
                                prune = int(indep[3]),
                                wriggle = int(indep[4]))
  tree.min = int(indep[5])
  tree.infoPrune = int(indep[6])
  tree.variancePrune = int(indep[7])
  tree.m = int(indep[6])
  tree.n = int(indep[7])
  prune = int(indep[8])
  return whereParm, tree

def model():
 trainDat, testDat = explore(dir = 'Data/')
#  set_trace()
 def f1(rows):
  indep = rows[1:-1]; case = 0
  # set_trace()
  whereParm, tree = update(indep)
  [test, train] = tdivPrec(where = None, dtree = tree, train = trainDat[1], test = testDat[1]);
  g = _runAbcd(train = train, test = test, verbose = False)
  return g

 return Cols(model,
        [N(least = 0, most = 5)
        , N(least = 2, most = 3)
        , N(least = 4, most = 6)
        , Bool(items = [True, False])
        , N(least = 0, most = 0.99)

        , N(least = 1, most = 10)
        , N(least = 1, most = 25)
        , N(least = 1, most = 10)
        , N(least = 1, most = 10)
        , O(f = f1)])

def _test():
  m = model()
  for _ in range(10):
    one = m.any()
    m.score(one)
    print(one)

def _de():
 "DE"
 DE = diffEvol(model = model);
 res = sorted([k for k in DE.DE()],
              key = lambda F: F[-1])[-1]
 return update(res[1:-1])

def main(dir = None):
  whereParm, tree = None, None  # _de()
  G = []; G1 = []; reps = 1;
  trainDat, testDat = explore(dir = 'Data/')
  for _ in xrange(reps):
    print reps
    [test, train] = tdivPrec(whereParm, tree, train = trainDat[1], test = testDat[0]);
    g = _runAbcd(train = train, test = test, verbose = False)
    G.append(g)
  G.insert(0, 'DT  ')

  for _ in xrange(reps):
    print reps
    [test, train] = tdivPrec1(whereParm, tree, train = trainDat[1], test = testDat[0]);
    g = _runAbcd(train = train, test = test, verbose = False)
    G1.append(g)
  G1.insert(0, 'C4.5')
  return [G, G1]

if __name__ == '__main__':
 print main()
 import sk; xtile = sk.xtile
 print xtile(G)

 # main(dir = 'Data/')
