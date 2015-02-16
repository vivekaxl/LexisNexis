import random
import argparse,re

def defaults(d,defaults):
  for k in d:
    if not k in defaults:
      print "bad",k
  for k,v in defaults.items():
    if not k in d:
      d[k] = v
  return d

def asd(parse,d0,**d):
  d = defaults(d,d0)
  dest = d['dest'] or re.sub(r'^--','',d['flag'])
  parse.add_argument(p['flag'], dest=d['dest'],
                     type=d['type'], help=d['help'],
                     default=d['default'])

def opts(about,*spec):
  d0 = dict(type=str,help="",default="",dest=None))
  parser = argparse.ArgumentParser(description=about)
  for spec in specs:
    asd(parse,d0,spec)
  return parse

opts("I love arthur",

"--love sad:float=1 asasdasddas"


     
