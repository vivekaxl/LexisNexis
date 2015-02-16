"""
ndiv: standard-division of numerics .
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved. 
      _____                                _______
    ,/_    ``-._                          /       \ 
   ,|:          `'-..__               ___|         |_
  ,|:_                 ``'''-----''''`_::~-.......-'~\ 
 ,|:_                                 _:    . ' .    :
 |:_                                  _:  .   '   .  |
 |:_                                  _:  '   .   '  |
 |:_                                  _:    ' . '    :
 |:_                    __,,...---...,,:_,.-'''''-.,_/
 |:_              _,.-``                 |         |
 |:_           ,-`                       |         |
 |:_         ,`                          |         |
 `|:_      ,'                            |         |
  |:_     /                              |         |
  `|:_   /                               |         |
   `|:_ :                                |         |
     \: |                                |         |
      \:|                                |         | cjr
       ~                                             

""" 

import sys,random
sys.dont_write_bytecode = True

def ndiv(lst, tiny=3,cohen=0.3,
         num=lambda x:x[0]):
  "Divide lst of (num,something) using means of nums"
  #----------------------------------------------
  class Counts(): # Add/delete counts of numbers.
    def __init__(i,inits=[]):
      i.zero()
      for number in inits: i + number 
    def zero(i): i.n = i.mu = i.m2 = 0.0
    def sd(i)  : 
      if i.n < 2: return i.mu
      else:       
        return (max(0,i.m2)*1.0/(i.n - 1))**0.5
    def __add__(i,x):
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/(1.0*i.n)
      i.m2 += delta*(x - i.mu)
    def __sub__(i,x):
      if i.n < 2: return i.zero()
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)   
  #----------------------------------------------
  def divide(this,small): #Find best divide of 'this'
    lhs,rhs = Counts(), Counts(num(x) for x in this)
    n0, mu, most, cut = 1.0*rhs.n, rhs.sd(), -1, None
    for j,x  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*(lhs.mu - mu)**2+ rhs.n/n0*(rhs.mu -mu)**2
        if maybe > most :      
          if abs(lhs.mu - rhs.mu) >= small:
            cut,most = j,maybe
      rhs - num(x)
      lhs + num(x)    
    return cut,most
  #----------------------------------------------
  def recurse(this, small,cuts):
    cut,sd = divide(this,small)
    if cut: 
      recurse(this[:cut], small, cuts)
      recurse(this[cut:], small, cuts)
    else:   
      cuts += [(sd,this)]
    return cuts
  #---| main |-----------------------------------
  small= Counts(num(x) for x in lst).sd()*cohen
  if lst: 
    return recurse(sorted(lst,key=num),small,[])

def _ndiv():
  "Demo code to test the above."
  import random
  bell= random.gauss
  random.seed(1)
  def go(lst,cohen=0.3,num=lambda x:x[0],tiny=3):
    print ""; print sorted(lst)[:10],"..."
    for d in  ndiv(lst,cohen=cohen,num=num,tiny=tiny):
        print num(d[1][0])
  l = [ (1,10), (2,11),  (3,12),  (4,13),
       (20,20),(21,21), (22,22), (23,23), (24,24),
       (30,30),(31,31), (32,32), (33,33),(34,34)]
  go(l,cohen=0.3)
  l = [62 , 66 , 69 , 69 , 69 , 72 , 72 , 72 , 76 , 76 , 79
     , 82 , 82 , 85]
  go(l,cohen=0.3,num= lambda x: x,tiny=3)
  l = [ 67 , 72 , 82 , 72 , 98 , 93 , 93 , 93 , 82 ,
       72 , 93 , 77 , 87 , 87 ]
  go(l,cohen=0.3,num= lambda x: x,tiny=3)
  ten     = lambda: bell(10,2)
  twenty  = lambda: bell(20,2)
  thirty  = lambda: bell(30,2)
  l=[]
  for _ in range(1000): 
    l += [(ten(),   ten()), 
          (twenty(),twenty()),
          (thirty(),thirty())]
  go(l,cohen=0.5,tiny=4000**0.5)
  


if __name__ == '__main__': _ndiv()

"""
Output:

[ (1, 10),  (2, 11),  (3, 12),  (4, 13), 
 (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), 
 (30, 30)] ...
1
20
30

[(3.7000699679075257, 13.718816007599141), 
 (3.815015386011323, 7.222657539933019), 
 (4.207498112954239, 10.56596537668784), 
 (4.328418426639925, 9.920222370615866), 
 (4.715076966608875, 10.343126948569484), 
 (4.78790689427217, 8.306688616563584), 
 (5.013513775695802, 6.965741666232676), 
 (5.030668572838251, 8.546550180016057), ...] ...
3.70006996791
14.9850387857
25.6550191106

"""
