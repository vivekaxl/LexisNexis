import sys,random
sys.dont_write_bytecode = True
rand=random.random

class Counts(): # Add/delete counts of numbers.
  def __init__(i,inits=[]):
    i.n = i.mu = i.m2 = 0.0
    for number in inits: i + number 
  def __add__(i,x):
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  def __sub__(i,x):
    if i.n > 1:
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)    
  def sd(i): return (i.m2*1.0/(i.n - 1))**0.5

f   = [0.0439301975,	0.8884841849,	0.315628067,	0.1508688607,	0.7760332984	,
       0.0808971641,	0.5327312081,	0.5017173954,	0.3727895041	,0.1248002942]

rhs = Counts(f)
lhs = Counts()

for i,f1 in enumerate(f):
  lhs + f1
  if lhs.n > 2: 
    print i, lhs.mu,lhs.sd()

for j,f1 in enumerate(reversed(f)):
  rhs - f1
  if rhs.n > 2: 
    print j, rhs.mu, rhs.sd()


