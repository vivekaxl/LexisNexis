from __future__ import division
from log import *
import sys, random, math, datetime, time,re, pdb
sys.dont_write_bytecode = True


exp = math.e
sqrt = math.sqrt
sin = math.sin
cos = math.cos
pi = math.pi

class Model:
  def name(i):
    return i.__class__.__name__
  def setup(i):
    # i.min = 10**(5)
    # i.max = -10**(5)
    i.xy = Options(x = [i.generate_x], y = [i.f1, i.f2]) # cahnge i.generate_x() to i.generate_x, any issues hereafter??
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) # hardcode 2
    i.history = {} # hold all logs for eras
  def generate_x(i):  
    x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    return x
  def getDepen(i, xlst):
    # y = [i.f1, i.f2]
    return sum([f(xlst) for f in i.xy.y])
  def getDepenlst(i, xlst):
    return [f(xlst) for f in i.xy.y]
  def cloneModel(i): # from Dr.Menzies'
    return i.__class__()
  def logxy(i, x):
    for val, log in zip(x, i.log.x): log += val
    y = i.getDepenlst(x)
    for val, log in zip(y, i.log.y): log += val
  def better(news,olds): # from Dr.Menzies'
    def worsed():
      return  ((same     and not betterIqr) or 
               (not same and not betterMed))
    def bettered():
      return  not same and betterMed
    out = False
    for new,old in zip(news.log.y, olds.log.y):
      betterMed, same, betterIqr = new.better(old)
      # print betterMed, same, betterIqr
      # pdb.set_trace()
      if worsed()  : return False # never any worsed
      if bettered(): out= out or True # at least one bettered
    return out
  def sa_neighbor(i, old):  
    p = 1/i.n
    new = old[:]
    for j in range(len(old)):
      if random.random() < p:
      	new_gen = i.generate_x()
        new[j] = new_gen[random.randint(0, i.n-1)]   
    return new
  def mws_neighbor(i,solution):  
    lo = 10**5
    hi = -10**5
    optimized_index = random.randint(0, len(solution)-1)
    if isinstance(i.hi,int):
      hi = i.hi
      lo = i.lo
    if isinstance(i.hi, list):
      hi = i.hi[optimized_index]
      lo = i.lo[optimized_index]
    increment = (hi - lo) /10
    temp_min = i.norm(i.getDepen(solution))
    temp_solution = solution[:]
    # print "old solution : %s" % solution
    # print "old norm energy : %s" % i.norm(i.getDepen(solution))
    for _ in range(10):
      temp_solution[optimized_index] = lo + increment
      temp = i.norm(i.getDepen(temp_solution))
      if temp < temp_min:
        temp_min = temp
        solution = temp_solution[:]
    # print "new solution : %s" % solution
    # print "new norm energy : %s" %i.norm(i.getDepen(solution))
    return solution
  def baseline(i):
  # model = eval(model+"()")
    i.min = 10**(5)
    i.max = -10**(5)
    for _ in xrange(Settings.other.baseline):
      temp = i.getDepen(i.generate_x())
      if temp > i.max:
        i.max = temp
      if temp < i.min:
        i.min = temp
    return i.min, i.max
  def norm(i, x):
    e = (x - i.min)/(i.max - i.min)
    return max(0, min(e,1)) #avoid values <0 or >1
  def trim(i, x, n ):
    return max(i.lo, min(x, i.hi))

class Control(object): # based on Dr.Menzies' codes
  def __init__(i, model, history = None):
    i.kmax = Settings.sa.kmax
    i.era = Settings.other.era
    i.lives = Settings.other.lives
    i.history = {} if history == None else history
    i.logAll = {}
    i.model = model
  def __call__(i, k):
    i.next(k)
  def logxy(i, results):
    both = [i.history, i.logAll, i.model.history]
    for log in both:
      if not i.era in log:
        log[i.era] = i.model.cloneModel()
    for log in both:
      log[i.era].logxy(results)
  def checkimprove(i):
      if len(i.logAll) >= 2:
        current = i.era
        before = i.era - Settings.other.era
        currentLog = i.logAll[current]
        beforeLog = i.logAll[before]
        # pdb.set_trace()
        if not currentLog.better(beforeLog):
          pass
        else:
          i.lives += 1
  def next(i, k):  
    if k >= i.era:
      i.checkimprove()
      i.era +=Settings.other.era
      if i.lives == 0:
        return True
      else:
        i.lives -=1
        return False



'''Schaffer'''
class Schaffer(Model):
  def __init__(i):
    i.lo = -5
    i.hi = 5
    i.n = 1
    i.fn = 2
    i.setup()
  def f1(i, x):
    return x[0] * x[0]
  def f2(i, x):
    return (x[0]-2) ** 2

'''Fonseca'''
class Fonseca(Model):
  def __init__(i):
    i.lo = -4
    i.hi = 4
    i.n = 3
    i.fn = 2
    i.setup()
  # def f1(i, xlst):
  #   return (1 - exp**(-1 * sum([(xlst[k] - 1/sqrt(i.n))**2 for k in xrange(i.n)])))
  # def f2(i, xlst):
  #   return (1 - exp**(-1 * sum([(xlst[k] + 1/sqrt(i.n))**2 for k in xrange(i.n)])))
  def f1(i, xlst):
    def f1_sum(x_list, n):
      value = []
      for item in x_list:
        value.append((item - 1/math.sqrt(n))**2)
      return sum(value)
    return 1 - math.e ** (-1* f1_sum(xlst, i.n))
  def f2(i,xlst):
    def f2_sum(x_list, n):
      value = []
      for item in x_list:
        value.append((item + 1/math.sqrt(n))**2)
      return sum(value)  
    return 1 - math.e ** (-1* f2_sum(xlst, i.n))
    
'''Kusarvs'''
class Kursawe(Model):
  def __init__(i):
    i.lo = -5
    i.hi = 5
    i.n = 3
    i.fn = 2
    i.setup()
  def f1(i, xlst):
    return sum([-10*exp**(-0.2 * sqrt(xlst[k]**2 + xlst[k+1]**2)) for k in xrange(i.n -1)])
  def f2(i, xlst):
    a = 0.8
    b = 3
    return sum([abs(x)**a + 5*sin(x)**b for x in xlst]) 

'''ZDT1'''
class ZDT1(Model):
  def __init__(i):
    i.lo = 0
    i.hi = 1
    i.n = 30
    i.fn = 2
    i.setup()
  def f1(i, xlst):
    return xlst[0]
  def f2(i, xlst):
    return (1 + 9 * (sum(xlst[1:]))/(i.n-1))
  # def f2(i,xlst):
  #   g1 = i.g(xlst)
  #   return g1*(1-sqrt(xlst[0]/g1))

'''ZDT3'''
class ZDT3(Model):
  def __init__(i):
    i.lo = 0
    i.hi = 1
    i.n = 30
    i.fn = 2
    i.setup()
  def f1(i, xlst):
    return xlst[0]
  def g(i, xlst):
    return (1 +  (9/(i.n-1)) * sum(xlst[1:]))
  def h(i,f1,g):
    return (1 - sqrt(f1/g) - f1/g) * sin(10 * pi * f1)
  def f2(i, xlst):
    return i.g(xlst) * i.h(i.f1(xlst),i.g(xlst)) 

'''Viennet3'''
class Viennet3(Model):
  def __init__(i):
    i.lo = -3
    i.hi = 3
    i.n = 2
    i.fn = 3
    i.setup1()
  def setup1(i):
    i.min = 10**(5)
    i.max = -10**(5)
    i.xy = Options(x = [i.generate_x()], y = [i.f1, i.f2, i.f3])
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) # hardcode 2
    i.history = {} # hold all logs for eras
  def f1(i, xlst):
    xy2 = xlst[0]**2 + xlst[1]**2
    return 0.5* (xy2) + sin(xy2)
  def f2(i, xlst):
    x = xlst[0]
    y = xlst[1]
    return ((3*x -2*y +4)**2/8 + (x-y+1)**2/27 + 15)
  def f3(i, xlst):
    xy2 = xlst[0]**2 + xlst[1]**2
    return (1/(xy2+1) - 1.1* exp**(-xy2))

  '''DTLZ7'''
class DTLZ7(Model):
  def __init__(i):
    i.M = 20
    i.K = 20
    i.lo = 0
    i.hi = 1
    i.n = i.M + i.K -1
    i.fn = i.M
    i.setup()
  def fi(i, x): # the frist one is x[0]
    return x
  def fm(i, xh=0):
    return (1 + i.g())*i.h()
  def g(i):
    return 1 + (9/i.K) * sum(i.xy.x[:i.M-1]) 
  def h(i):
    sumtemp = 0
    for n,x in enumerate(i.xy.x):
      if n ==i.M-2:
        break
      sumtemp +=(i.xy.y[n](x)/(1.0+i.g()))*(1+sin(3.0*pi*i.xy.y[n](x)))
    return (i.M - sumtemp)# k = 0,...., M-2
  def setup(i):
    tempx = i.generate_x()
    tempy = [i.fi for k in tempx[:-1]]
    tempy.append(i.fm)
    i.xy = Options(x = tempx, y = tempy)
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) 
    i.history = {} # hold all logs for eras
    # i.min = 10**(5)
    # i.max = -10**(5)
  def getDepen(i, xlst):
    temp = i.fm()
    return sum(xlst[:i.M])+temp

  def getDepenlst(i, xlst):
    return xlst[:i.M]+ [i.fm()]

    '''Schwefel's'''
class Schwefel(Model):
  def __init__(i):
    i.lo = -pi
    i.hi = pi
    i.n = [10,20, 40][0]
    i.f_bias = -460
    i.fn = 1
    i.randI = lambda x: random.randint(-x, x)
    i.randF = lambda x: random.uniform(-x, x)
    i.a = [[i.randI(100) for _ in xrange(i.n)] for _ in xrange(i.n)] # matrix for a
    i.b = [[i.randI(100) for _ in xrange(i.n)] for _ in xrange(i.n)] # matrix for b
    i.alpha = [i.randF(pi) for _ in xrange(i.n)] # alpha
    i.setup()
  def f(i, x):
    F = sum([(i.A(n) - i.B(x,n))**2 for n in xrange(i.n)]) + i.f_bias
    return F
  def A(i,n):
    sumA = sum([i.a[n][j]*sin(i.alpha[j]) + i.b[n][j] * cos(i.alpha[j]) for j in xrange(i.n)])
    return sumA
  def B(i, x,n):
    sumB = sum([i.a[n][j]*sin(s) + i.b[n][j]* cos(s) for j,s in enumerate(x)])
    return sumB
  def setup(i):
    i.min = 10**(5)
    i.max = -10**(5)
    i.xy = Options(x = [i.generate_x()], y = [i.f])
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) 
    i.history = {} # hold all logs for eras

  '''Osyczka'''
class Osyczka(Model):
  def __init__(i):
    i.lo = [0, 0, -1, 0, 1, 0]
    i.hi = [10, 10, 5, 6, 5, 10]
    i.fn = 2
    i.n = 6
    i.setup()

  def generate_x1x2(i):
    def g1(x):
      return x[0] + x[1] - 2 >= 0
    def g2(x):
      return 6 - x[0] - x[1] >= 0
    def g3(x):
      return 2 - x[1] + x[0] >= 0
    def g4(x):
      return 2 - x[0] + 3* x[1] >= 0
    while 1:
      x= [i.lo[n] + (i.hi[n]-i.lo[n])*random.random() for n in range(2)]
      if g1(x) and g2(x) and g3(x) and g4(x):
        return x
      else:
        continue

  def generate_x3456(i):
    def g5(x):
      return 4 - (x[0]- 3)**2 - x[1] >= 0
    def g6(x):
      return (x[2] - 3)**2 + x[3] - 4 >= 0
    while 1:
      x= [i.lo[n] + (i.hi[n]-i.lo[n])*random.random() for n in range(2,6)]
      if g5(x) and g6(x):
        return x
      else:
        continue

  def generate_x(i):
    x12 = i.generate_x1x2()
    x3456 = i.generate_x3456()
    x = x12 + x3456 
    return x

  def f1(i, x):
    result = -25*(x[0] -2) **2 - (x[1] - 2)**2 - (x[2] - 1)**2 - (x[3] - 4) **2 -(x[4] -1) **2
    return result

  def f2(i, x):
    result = sum([i**2 for i in x])
    return result
  def trim(i, x, n):
    return max(i.lo[n], min(x, i.hi[n]))



