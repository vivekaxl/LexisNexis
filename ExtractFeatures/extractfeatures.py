import ast
dictnames = {}
class v(ast.NodeVisitor):
  def generic_visit(self, node):
  	try:
  		dictnames[type(node).__name__] += 1
  	except:
  		dictnames[type(node).__name__] = 1
  	ast.NodeVisitor.generic_visit(self, node)
  def visit_Load(self, node): pass

def get_names(dir_name):
  import glob,os
  name = dir_name+"/*.py"
  filelist = glob.glob(name)
  return sorted(filelist)

def test():
  source_file = "deadant.py"
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
  preprocessing()
  from collections import defaultdict
  collector = defaultdict(dict)
  features = set()
  folks = ['george','jim','naveen','rahul','timm','vivekaxl','wei']
  for f in folks: movefiles(f)
  for tps in folks:
    storage ={}
    source_files = get_names(tps)
    for source_file in source_files:
      print tps,source_file
      try:
        f = open(source_file,"r")
        x = v()
        t = ast.parse(f.read())
        x.visit(t)
      except:
        continue
      normalize = sum([dictnames[x] for x in dictnames.keys()])
    for x in dictnames.keys():
      storage[x] = float(dictnames[x])/normalize
    collector[tps] = storage
  for c in collector.keys():features.update(collector[c].keys())
  
  for f in features:
    print f,
    for c in collector.keys():
      try:
        print collector[c][f],
      except:
        print "0",
    print

  print "========================================="
  for c in collector.keys():
    test = []
    for f in features:
      try:
        test.append(collector[c][f])
      except:
        test.append(0)
    print entropy(test)




