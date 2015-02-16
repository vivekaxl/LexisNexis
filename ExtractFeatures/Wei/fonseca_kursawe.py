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
    
'''kusarvs'''
class kursawe:
  def __init__(i):
    i.lo = -5
    i.hi = 5
    i.n = 3
    
  def gen(i):
    return generate(i.lo, i.hi, i.n)
    
  def f1_plus_f2(i, x_list):
    n = i.n  
    def f1_inner(x_list, n):
      value = []
      for i in range(n-1):
        value.append(-10 * math.e **(-0.2 * math.sqrt(x_list[i]**2 + x_list[i+1]**2)))
      return value
    
    def f2_inner(x_list, n):
	  value = []
	  a = 0.8
	  b = 3
	  for item in x_list:
		value.append(abs(item)**a + 5 * math.sin(item)**b )
	  return value
    f1 = sum(f1_inner(x_list, n))
    f2 = sum(f2_inner(x_list, n))
	#   print f1+f2
    return f1+f2



'''hello'''
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


def energy(x, min, max):
  e = (x - min)/(max - min)
  return e
# 

def neighbor(old, generator):  # can put in to generator
  for i in range(len(old)):
    if random.random() <=0.33:
      old[i] = generator.generate_x()[i] 
  return old
      
def P(old, new, t):
  prob = math.e**((old - new)/t) 
  return prob    
      
def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()
      
def sa():
  model_str = raw_input("Type 1 for fonseca and 2 for kursawe:")
  if (model_str) == '1':
    model = fonseca()
  elif (model_str) == '2':
	model = kursawe()
  else:
    print "please type 1 or 2!"
    exit()
#   model = ()
#   model = kursawe()
#   x = generate(model.lo, model.hi, model.n)
  generator = model.gen()
  min, max = find_max_min(model, generator)
#   print min, max
#   min, max = 0.98, 2.0
  s = generator.generate_x()
#   print s
  e = energy(model.f1_plus_f2(s), min, max)
#   print e
  sb = s
  eb = e
  k = 1
  kmax = 1000
  while k < kmax:
    sn = neighbor(s, generator)
    en = energy(model.f1_plus_f2(sn), min,max)
    if en < eb:
	  sb = sn
	  eb = en 
	  say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, (k/kmax)) < random.random():
      s = sn
      e = en
      say('?')
    say('.')
    k = k+1
    if k % 40 == 0: 
      print "\n"
      say(str(round(eb,3)))
#   print "\n"    
#   say(str(sb))
  return sb
#   




if __name__ == "__main__": sa()