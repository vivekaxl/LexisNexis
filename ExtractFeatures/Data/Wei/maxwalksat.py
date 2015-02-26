from __future__ import division
import sys, random, math
from common import *
import numpy as np
sys.dont_write_bytecode = True



random.seed(1)

class generate:
  def __init__(i, lo, hi, n):
    i.lo = lo
    i.hi = hi
    i.n = n
  def generate_x(i): 
    x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    return x

class fonseca:
  def __init__(i):
    i.lo = -4
    i.hi = 4
    i.n = 3
    
  def gen(i):
    return generate(i.lo, i.hi,i.n)
    
  def f1_plus_f2(i, x_list):
    n = i.n
#     print x_list
    def f1_sum(x_list, n):
	  value = []
	  for item in x_list:
	    value.append((item - 1/math.sqrt(n))**2)
	  return sum(value)

    def f2_sum(x_list, n):
	  value = []
	  for item in x_list:
	    value.append((item + 1/math.sqrt(n))**2)
	  return sum(value)  

    f1 = 1 - math.e ** (-1* f1_sum(x_list, n))
    f2 = 1 - math.e ** (-1* f2_sum(x_list, n))
#     print f1+f2
    return f1+f2
# def score():

def score(raw_energy, min, max):
  return(raw_energy - min)/(max - min)
  
def find_max_min(model, gen):
  # model = eval(model+"()")
  min = 10**(5)
  max = -10**(5)
  for i in range(100000):
    temp = model.f1_plus_f2(gen.generate_x())
    if temp > max:
      max = temp
    if temp < min:
	  min = temp
  return min, max
  
## score

def optimal_neighbor(solution, model, min, max):  
  optimized_index = random.randint(0, len(solution)-1)
  increment = (model.hi - model.lo)/10
  temp_min = 10*(5)
#   print "old solution : %s" % solution
  for _ in range(10):
    solution[optimized_index] = model.lo+increment
    temp = score(model.f1_plus_f2(solution), min, max)
    if temp < temp_min:
       temp_min = temp
#   print "new solution : %s" % solution
  return solution
    
#   for i in range(len(old)):
#     if random.random() <=0.3:
#       old[i] = generator.generate_x()[i] 
#   return old  
  
def maxwalksat():
  max_tries = 50
  max_changes = 2000
  model = fonseca()
  generator = model.gen()
  min, max = find_max_min(model, generator)
  threshold = 0.1
  total_loop = 0
  total_tries = 0
  final_score = 0
  p = 0.25
#   print threshold
#   
#   print solution
  for _ in range(max_tries):
    total_tries += 1
    solution = generator.generate_x() 
#     print 'try {0} time(s) with solution {1}'.format( total_tries, solution)
    for _ in range(max_changes):
      final_score=score(model.f1_plus_f2(solution),min, max)
#       print "final score: %s" % final_score
      if final_score <= threshold:
        print "p : %s" % p
        print "threshold : %s" %threshold
        print "total tries: %s" % total_tries
        print "total changes: %s" % total_loop
        print "min_energy:{0}, max_energy:{1}".format(min, max)
        print "min_energy_obtained: %s" % model.f1_plus_f2(solution)
        print "solution : %s" % solution
        print "score: %s" % final_score
        return solution
      if p < random.random():
        solution[random.randint(0,2)] = generator.generate_x()[random.randint(0,2)]
      else:
        solution = optimal_neighbor(solution, model, min, max)
      total_loop +=1  
    
#        c =  generator.generate_x() 
       
if __name__ =="__main__": maxwalksat()  
  

