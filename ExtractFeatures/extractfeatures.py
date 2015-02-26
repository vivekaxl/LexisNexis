import ast
dictnames = {}
library = {}
class v(ast.NodeVisitor):
  # def visit_Call(self,node):
  #   print "Called : ",node.func.id
  def visit_Import(self,node):
        for n in node.names:
              try:library[n.name] += 1
              except: library[n.name] = 1

  def visit_ImportFrom(self,node):

        if len(node.names) == 1  and str(node.names[-1].name) == "*":
              print ">>>>>>>>>>>>>>>>>>>>>>TRUE"
              try:library[node.module] += 1
              except: library[node.module] = 1
        else:
            for n in node.names:
              #print n.name, len(node.names),str(node.names[-1].name)
              try:library[n.name] += 1
              except: library[n.name] = 1


  def generic_visit(self, node):
    try:dictnames[type(node).__name__] += 1
    except: dictnames[type(node).__name__] = 1
    ast.NodeVisitor.generic_visit(self, node)
  def visit_Load(self, node): pass

def get_names(dir_name):
  import glob,os
  name = dir_name+"/*.py"
  filelist = glob.glob(name)
  return sorted(filelist)

def test():
  source_file = "./vivekaxl/xomo.py"
  f = open(source_file,"r")
  x = v()
  t = ast.parse(f.read())
  x.visit(t)

def preprocessing():
  import os
  path = get_filepaths(".") 
  path = [ x for x in path if x.endswith(".py") != True]
  for p in path: os.remove(p)

def movefiles(directory):
  import os
  path = get_filepaths("./"+directory) 
  path = [ x for x in path if x.endswith(".py")]

  for p in path: 
    os.rename(p,"./"+directory+"/"+p.split('/')[-1])
  removedirectories(directory)

def removedirectories(directory):
  import os
  for root,directories, files in os.walk(directory,topdown=False):
    for name in directories:
        os.rmdir("./" + os.path.join(root, name))


def get_filepaths(directory):
    import os
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

import math
from collections import Counter
def entropy(s):
  p, lns = Counter(s), float(len(s))
  return -sum( count/lns * math.log(count/lns, 2) for count in p.values())  



if __name__ == '__main__':
  global dictnames
  preprocessing()
  from collections import defaultdict
  collector = defaultdict(dict)
  library_collector = defaultdict(dict)
  features = set()
  libraries = set()
  #folks = ['Abhi0725', 'abhi92', 'abhik137', 'adamminter4', 'adityatj', 'ameenkhan07', 'aminator', 'apoorv74', 'arunshivaram', 'aryak93', 'bikurishita', 'bup', 'CarterPape', 'cgutshal', 'darthvish', 'datasaur', 'DestroyerAlpha', 'dgersting', 'digen', 'djadmin', 'dragonfly90', 'dremelofdeath', 'easyfly007', 'edu.dlf.refactoring.python', 'euphonogenizer', 'extractfeatures.py', 'Feb19', 'george', 'GeorgePanzerMathew', 'ghoiufyia', 'govg', 'Harishwar', 'Hexkbr', 'imanujagarwal', 'Indish', 'jayasth', 'jim', 'jmilinovich', 'jptiancai', 'jsinix', 'kelcecil', 'Kingson', 'kracekumar', 'liveashish', 'madratman', 'manojmj92', 'matheeeny', 'measures.py', 'Mike-Xie', 'milangupta511', 'mrafayaleem', 'naveen', 'Niharika29', 'nishant57', 'nkcsgexi', 'pareekrachit', 'peterk143', 'poryfly', 'prakashn27', 'prasanthlouis', 'pratik98', 'pulkitpahwa', 'raghuveerkancherla', 'rahimnathwani', 'rahlk', 'rahul', 'rakeshsukla53', 'rameshkopparapu', 'rcdosado', 'Research', 'revathskumar', 'rmad17', 'routeaccess', 'seowyanyi', 'shaharzeira', 'shenwei356', 'shrikrishnaholla', 'shyam057cs', 'skyrideraj', 'SmitBawkar', 'sohamchakravarty', 'sojan-official', 'stickster', 'SudShekhar', 'svakeeswaran', 'theGreatHeisenberg', 'thesantosh', 'timm', 'umangmathur92', 'unmarshal', 'vijetha35', 'vikas-parashar', 'vivekaxl', 'vjex', 'Wei', 'xiangshuai']
  import os, sys
  folks = os.listdir(".")
  for f in folks: movefiles(f)
  for tps in folks:
    storage ={}
    library_s = {}
    source_files = get_names(tps)
    dictnames ={}
    library = {}
    for source_file in source_files:
      #print tps,source_file
      try:
        f = open(source_file,"r")
        x = v()
        t = ast.parse(f.read())
        x.visit(t)
      except:
        print source_file
        pass
    normalize = sum([dictnames[x] for x in dictnames.keys()])
    library_normalize = sum([library[x] for x in library.keys()])

    #print tps
    #print dictnames
    for x in dictnames.keys():
      storage[x] = float(dictnames[x])/normalize
    for x in library.keys(): 
      library_s[x] = float(library[x])/library_normalize
    library_collector[tps] = library_s
    collector[tps] = storage



  for c in collector.keys():features.update(collector[c].keys())
  for l in library_collector.keys(): libraries.update(library_collector[l].keys())

  
  for f in features:
    print f,
    for c in collector.keys():
      try:
        print c,"|",collector[c][f],
      except:
        print "0",
    print

  print "========================================="

  for l in libraries:
    print l,
    for lc in library_collector.keys():
      try:
        print lc,"|",library_collector[lc][l],
      except:
        print "0",
    print

  # print "========================================="
  # for c in collector.keys():
  #   test = []
  #   for f in features:
  #     try:
  #       test.append(collector[c][f])
  #     except:
  #       test.append(0)
  #   print entropy(test)




