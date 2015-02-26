from __future__ import division 
import sys 
import random
import math 
import numpy as np
from where_mod import *
from models import *
from options import *
from utilities import *
sys.dont_write_bytecode = True

#say = Utilities().say


class SearchersBasic():
  tempList=[]
  def display(self,score,printChar=''):
    self.tempList.append(score)
    if(self.displayStyle=="display1"):
      print(printChar),
  
  def display2(self):
    if(self.displayStyle=="display2"):
      #print xtile(self.tempList,width=25,show=" %1.6f")
      self.tempList=[]

class MaxWalkSat(SearchersBasic):
  model = None
  minR=0
  maxR=0
  random.seed(40)
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS

      

  def evaluate(self):
    model = self.model
    #print "Model used: %s"%model.info()
    minR=model.minR
    maxR=model.maxR
    maxTries=int(myoptions['MaxWalkSat']['maxTries'])
    maxChanges=int(myoptions['MaxWalkSat']['maxChanges'])
    n=model.n
    threshold=float(myoptions['MaxWalkSat']['threshold'])
    probLocalSearch=float(myoptions['MaxWalkSat']['probLocalSearch'])
    bestScore=100
    bestSolution=[]


    #print "Value of p: %f"%probLocalSearch
   # model = Fonseca()
    #model.baseline(minR,maxR)
    #print model.maxVal,model.minVal
    
    for i in range(0,maxTries): #Outer Loop
      solution=[]
      for x in range(0,n):
        solution.append(minR[x] + random.random()*(maxR[x]-minR[x]))
      #print "Solution: ",
      #print solution  
      for j in range(1,maxChanges):      #Inner Loop
         score = model.evaluate(solution)
         #print score
         # optional-start
         if(score < bestScore):
           bestScore=score
           bestSolution=solution
           
         # optional-end
         if(score < threshold):
           #print "threshold reached|Tries: %d|Changes: %d"%(i,j)
           self.display(".",score),
           self.display2()
           self.model.evalBetter()    
           revN = model.maxVal-model.minVal
           return bestSolution,bestScore,self.model
         
         if(random.random() > probLocalSearch):
             c = int((self.model.n)*random.random())
             solution[c]=model.neighbour(minR,maxR,c)
             self.display(score,"+"),
         else:
             tempBestScore=score
             tempBestSolution=solution             
             c = int(self.model.n*random.random())
             interval = (maxR[c]-minR[c])/10
             for itr in range(0,10):                
                solution[c] = minR[c] + (itr*interval)*random.random()
                tempScore = model.evaluate(solution)
                if(tempBestScore > tempScore):     # score is correlated to max?
                  tempBestScore=tempScore
                  tempBestSolution=solution
             solution=tempBestSolution
             self.display(tempBestScore,"!"),
         self.display(score,"."),
         if(self.model.lives == 1):
           #print "DEATH"
           self.display2()
           self.model.evalBetter()
           revN = model.maxVal-model.minVal
           return bestSolution,bestScore,self.model
         
         if(j%50==0):
            #print "here"
            self.display2()
            self.model.evalBetter()
    revN = model.maxVal-model.minVal
    return bestSolution,bestScore,self.model      

def probFunction(old,new,t):
   return np.exp(1 *(old-new)/t)

class SA(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS


  def neighbour(self,solution,minR,maxR):
    returnValue = []
    n=len(solution)
    for i in range(0,n):
      tempRand = random.random()
      if tempRand <(1/self.model.n):
        returnValue.append(minR[i] + (maxR[i] - minR[i])*random.random())
      else:
        returnValue.append(solution[i])
    return returnValue

  def evaluate(self):
    model=self.model
    #print "Model used: %s"%(model.info())
    minR = model.minR
    maxR = model.maxR
    #model.baseline(minR,maxR)
    #print "MaxVal: %f MinVal: %f"%(model.maxVal, model.minVal)

    s = [minR[z] + (maxR[z] - minR[z])*random.random() for z in range(0,model.n)]
    #print s
    e = model.evaluate(s)
    emax = int(myoptions['SA']['emax'])
    sb = s                       #Initial Best Solution
    eb = e                       #Initial Best Energy
    k = 1
    kmax = int(myoptions['SA']['kmax'])
    count=0
    while(k <= kmax and e > emax):
      #print k,e
      sn = self.neighbour(s,minR,maxR)
      en = model.evaluate(sn)
      if(en < eb):
        sb = sn
        eb = en
        self.display(en,"."),#we get to somewhere better globally
      tempProb = probFunction(e,en,k/kmax)
      tempRand = random.random()
#      print " tempProb: %f tempRand: %f " %(tempProb,tempRand)
      if(en < e):
        s = sn
        e = en
        self.display(en,"+"), #we get to somewhere better locally
      elif(tempProb > tempRand):
        jump = True
        s = sn
        e = en
        self.display(en,"?"), #we are jumping to something sub-optimal;
        count+=1
      self.display(en,"."),
      k += 1
      if(self.model.lives == 0):
        self.display2()
        self.model.emptyWrapper()
        #print "out1" 
        revN = model.maxVal-model.minVal
        return sb,eb,self.model 
      
      if(k % 50 == 0):
         self.display2()
         self.model.evalBetter()
       #  print "%f{%d}"%(sb,count),
         count=0
    #print "out2"
    self.model.emptyWrapper()
    revN = model.maxVal-model.minVal
    return sb,eb,self.model

class GA(SearchersBasic):
  model = None
  minR=0
  maxR=0
  population={}
  random.seed(1)
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.crossoverRate = float(myoptions['GA']['crossOverRate'])
    self.mutationRate = 1/self.model.n
    self.elitismrank = int(myoptions['GA']['elitism'])
    self.generation = int(myoptions['GA']['generation'])

  def crossOver(self,listdaddy,listmommy):
    rate=self.crossoverRate
    #assert(len(listdaddy)==len(listmommy)),"Something's messed up"
    if(random.random()<rate):
      minR,maxR=0,len(listdaddy)
      tone = int(minR + random.random()*((maxR)-minR))
      ttwo = int(minR + random.random()*(maxR-(minR)))
      one,two=min(tone,ttwo),max(tone,ttwo)
      #print "CrossOver: %d %d "%(one,two)
      #if(one==two):two+=2+(minR+random.random()*(maxR-minR-two-2))
      newDaddy=listdaddy[:one]+listmommy[one:two]+listdaddy[two:]
      newMommy=listmommy[:one]+listdaddy[one:two]+listmommy[two:]
      return newDaddy,newMommy
    return listdaddy,listmommy

  def mutation(self,listdaddy,listmommy):
     rate=1#self.mutationRate
     #assert(len(listdaddy)==len(listmommy)),"Something's messed up"
     if(random.random() < rate):
       #print "MUTATION"
       mutant = listdaddy[:]
       minR,maxR=0,min(len(listdaddy),len(listmommy))
       mutationE = int(minR + (random.random()*(maxR-minR)))
       mutationH = int(minR + (random.random()*(maxR-minR)))
       #print "++ %f %f"%(len(listdaddy),len(listmommy))
       #print ">> %f %f"%(mutationE,mutationH)
       mutant[mutationE]=listmommy[mutationH]
       return mutant
     return listdaddy
  
  #Changes a list of numbers to a stream of numbers
  #eg. [0.234,0.54,0.54325] -> [2345454325]
  def singleStream(self,listpoints):
     singlelist=[]
     for i in listpoints:
       tempstr = str(i)[2:]
       for x in tempstr:
         singlelist.append(x)
     #print singlelist
     return singlelist 

  def generate(self):
    minR = self.model.minR
    maxR = self.model.maxR
    #http://stackoverflow.com/questions/4119070/
    #how-to-divide-a-list-into-n-equal-parts-python
    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    model=self.model
    minR = model.minR
    maxR = model.maxR
    #model.baseline(minR,maxR)
    temps1 = self.Roulette(self.population)
    temps2 = self.Roulette(self.population)
    #workaround: Bug: was getting e in temp2 so,
    #whenever I see anything other than 0-9
    #I replace it
    try:
      import re 
      temps1 = re.sub('[^0-9]', '', temps1)
      temps2 = re.sub('[^0-9]', '', temps2)
    except:
      print temps1
      print temps2
      raise Exception("Ouch!")
    s1 = map(int, temps1)[:self.model.n]
    s2 = map(int, temps2)[:self.model.n]
    #print "S1,S2: %d %d " %(len(s1),len(s2))
    c1,c2=self.crossOver(s1,s2)
    #print "C1,C2: %d %d " %(len(c1),len(c2))
    m1 = self.mutation(c1,c2)
    m2 = self.mutation(c2,c1)
    #print "M1,M2: %d %d " %(len(m1),len(m2))
    #print "self.model.n: %d"%model.n
    normalc1 = [int(''.join(map(str,x)))/10**len(x) for x in lol(m1,1)]
    normalc2 = [int(''.join(map(str,x)))/10**len(x) for x in lol(m2,1)]
    #print "normalc1,normalc2: %d %d"%(len(normalc1),len(normalc2))
    #normalc1 = map(lambda x:minR+x*(maxR-minR),normalc1)    
    #normalc2 = map(lambda x:minR+x*(maxR-minR),normalc2)
    if(len(normalc1)>=self.model.n and len(normalc2)>=self.model.n):
      return normalc1[:self.model.n],normalc2[:self.model.n]  #workaround
    else:
      #print "eeeeeeeeeeee>>>>>>>>>>>>>>>>>>>>>>>>eeeeeeehaha"
      str1 = [random.random() for z in range(0,self.model.n)]
      normalc1,normalc2=[],[]
      for ij in xrange(len(str1)):
        normalc1.append(minR[ij]+str1[ij]*(maxR[ij]-minR[ij]))
      str2 = [random.random() for z in range(0,self.model.n)]  
      for ij in xrange(len(str2)):
        normalc2.append(minR[ij]+str1[ij]*(maxR[ij]-minR[ij]))
      #normalc2 = map(lambda x:minR+x*(maxR-minR),str2)
      return normalc1,normalc2

  #http://stackoverflow.com/questions/10324015
  #/fitness-proportionate-selection-roulette-wheel-selection-in-python
  def Roulette(self,choices):
    maxN = sum(choices.values())
    pick = random.uniform(0, maxN)
    current = 0
    for key, value in choices.items():
        current += abs(value)
        if current > abs(pick):
            return key
    print "Ouch!!"
    print pick,maxN
  
  def keyTransform(self,s):
    minR = self.model.minR
    maxR = self.model.maxR
    strs = self.singleStream(s)
    strs = (''.join(map(str,strs)))
    temp=[]
    for i in xrange(len(s)):
      temp.append(minR[i]+s[i]*(maxR[i]-minR[i]))
    fitness = self.model.evaluate(temp)
    return strs,fitness

  def initialPopulation(self):
    model=self.model
    for i in xrange(50):
      s = [random.random() for z in range(0,model.n)]
      strs,fitness = self.keyTransform(s)
      self.population[strs]=fitness

  def elitism(self):
    rank = self.elitismrank
    #print len(self.population),
    #This controls whether this GA maximizes
    #or minimizes
    l = sorted(self.population.values())
    l = l[rank:]
    # TODO: not at all efficient
    for i in l:
      self.population = {key: value \
      for key, value in self.population.items() \
             if value is not i}
    #print len(self.population)
     

  def evaluate(self):
    #print "evaluate>>>>>>>>>>>>>>>>>>>>>>>>>"
    bestSolution=[]
    bestScore = 1e6
    done=False
    model=self.model
    #print "Model used: %s"%(model.info())
    minR = model.minR
    maxR = model.maxR
    #model.baseline(minR,maxR)
    #print "MaxVal: %f MinVal: %f"%(model.maxVal, model.minVal)
    #print "n: %d"%model.n
    self.initialPopulation()
    #print "initial population generated"
    for x in xrange(self.generation):
      #print "Generation: %d"%x
      #print "#",
      for i in xrange(20):
        s1,s2 = self.generate()
        #TODO: dirty
        strs,fitness = self.keyTransform(s1)
        self.population[strs]=fitness
        strs,fitness = self.keyTransform(s2)
        self.display(score=fitness)
        self.population[strs]=fitness
        if(fitness<bestScore):
          bestScore=fitness
          bestSolution=strs
        #print "child born"
      self.model.evalBetter()
      self.elitism()
      #self.display2()
      if(self.model.lives == 0):
        self.display2()
        self.model.emptyWrapper()
        lol = lambda lst, sz: [lst[i:i+sz] \
        for i in range(0, len(lst), sz)]
        tempSolution = [int(''.join(map(str,x)))/10**len(x)\
        for x in lol(bestSolution,int(len(bestSolution)/model.n))]
        solution=[]
        for ij in xrange(len(tempSolution)):
          solution.append(minR[ij]+tempSolution[ij]*(maxR[ij]-minR[ij]))
        #solution= map(lambda x:minR+x*(maxR-minR),tempSolution) 
        return solution,bestScore,self.model

      
    #print sorted(self.population.values())
    self.model.emptyWrapper()
    lol = lambda lst, sz: [lst[i:i+sz] \
    for i in range(0, len(lst), sz)]
    tempSolution = [int(''.join(map(str,x)))/10**len(x)\
     for x in lol(bestSolution,int(len(bestSolution)/model.n))]
    solution= map(lambda x:minR+x*(maxR-minR),tempSolution) 
    return solution,bestScore,self.model

class DE(SearchersBasic):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model=modelName
    self.displayStyle=displayS
    self.model.minVal = bmin
    self.model.maxVal = bmax

  def threeOthers(self,frontier,one):
    #print "threeOthers"
    seen = [one]
    def other():
      #print "other"
      for i in xrange(len(frontier)):
        while True:
          k = random.randint(0,len(frontier)-1)
          #print "%d"%k
          if frontier[k] not in seen:
            seen.append(frontier[k])
            break
        return frontier[k]
    this = other()
    that = other()
    then = other()
    return this,that,then
  
  def trim(self,x,i)  : # trim to legal range
    m=self.model
    return max(m.minR[i], min(x, m.maxR[i]))      

  def extrapolate(self,frontier,one,f,cf):
    #print "Extrapolate"
    two,three,four = self.threeOthers(frontier,one)
    #print two,three,four
    solution=[]
    for d in xrange(self.model.n):
      x,y,z=two[d],three[d],four[d]
      if(random.random() < cf):
        solution.append(self.trim(x + f*(y-z),d))
      else:
        solution.append(one[d]) 
    return solution

  def update(self,m,f,cf,frontier,minScore=1e6,total=0.0,n=0):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
      max(lo(m,i), x%hi(m,i))
    def better(old,new):
      assert(len(old)==len(new)),"Length mismatch"
      for i in xrange(len(old)-1): #Since the score is return as [values of all objectives and energy at the end]
        if old[i] > new[i]: pass
        else: return False
      return True
    changed = False
    model=self.model
    newF = []
    total,n=0,0
    for x in frontier:
      s = model.evaluate(x)[:-1]
      new = self.extrapolate(frontier,x,f,cf)
      #print new
      tnew = [] 
      for i,j in enumerate(new):
        tnew.append(trim(m,j,i))
      #assert(len(tnew) == 20),"mismatch"
      newe=model.evaluate(new)[:-1]
      if better(s,newe) == True and s[-1] > newe[-1]:
        newF.append(tnew)
        changed = True
      else:
        newF.append(x)
    return newF,changed
      
  def evaluate(self,repeat=100,np=100,f=0.75,cf=0.3,epsilon=0.01,lives=4):
    #print "evaluate"
    model=self.model
    minR = model.minR
    maxR = model.maxR
    #model.baseline(minR,maxR)
    frontier = [[model.minR[i]+random.random()*(model.maxR[i]-model.minR[i]) for i in xrange(model.n)]
               for _ in xrange(np)]
    for i in xrange(repeat):
      if lives == 0: break
      frontier,changed = self.update(model,f,cf,frontier)

      self.model.evalBetter()
      if changed == False: 
        lives -= 1
        print "lost it"
    minR=9e10
    for x in frontier:
      #print x
      energy = self.model.evaluate(x)[-1]
      if(minR>energy):
        minR = energy
        solution=x 
    return solution,minR,self.model

class PSO(SearchersBasic):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.v = []
    self.p = []
    self.lb = []
    self.gb = [self.model.minR[i] + random.random()*(self.model.maxR[i]-self.model.minR[i]) \
    for i in xrange(self.model.n)]
    self.eb=self.model.evaluate(self.gb)
    self.displayStyle=displayS 
    self.phi1=myoptions['PSO']['phi1']
    self.phi2=myoptions['PSO']['phi2']
    self.W=myoptions['PSO']['W']
    self.N=myoptions['PSO']['N']
    self.Repeat=myoptions['PSO']['repeat']    
    self.threshold=myoptions['PSO']['threshold'] 
    for x in xrange(self.N):
      self.v.append([0 for _ in xrange(self.model.n)])
      self.p.append([self.model.minR[i] + random.random()*(self.model.maxR[i]-self.model.minR[i])\
      for i in xrange(self.model.n)])
      self.lb.append(self.p[x])
      if(self.model.evaluate(self.p[x])<self.model.evaluate(self.gb)):
        self.gb = self.p[x]
        self.eb = self.model.evaluate(self.gb)
  
  def trim(self,x,i)  : # trim to legal range
    m=self.model
    return max(m.minR[i], min(x, m.maxR[i]))  
  
  def velocity(self,v,p,lb,gb):

    newv = [self.K*(self.W*v[i]+self.phi1*random.random()*(lb[i]-p[i])\
           +self.phi2*random.random()*(gb[i]-p[i])) for i in xrange(self.model.n)]
    #print "blah1"
    return newv

  def displace(self,v,p):
    newp = [v[i]+p[i] for i in xrange(self.model.n)]
    #print "NEWP: ",newp
    return [self.trim(newp[i],i) for i in xrange(len(newp))] 

  def evaluate(self,N=30,phi1=1.3,phi2=2.8,w=1):

    model=self.model 
    v= self.v
    p= self.p 
    lb= self.lb 
    gb= self.gb
    #print "GB: "%gb
    #print "evaluate"
    phi1=self.phi1
    phi2=self.phi2
    N=self.N
    W=self.W
    Repeat=self.Repeat
    threshold=float(self.threshold)
    eb=10**6
    minR = model.minR
    maxR = model.maxR
    phi = phi1+phi2
    self.K = 2/(abs(2 - (phi) -math.sqrt(phi **2) -4*phi))
    #model.baseline(minR,maxR)

    for i in xrange(Repeat):
      #if(i%998):print "boom"     
      if(eb<threshold):
        return 0,eb,model
      for n in xrange(N):
        v[n]=self.velocity(v[n],p[n],lb[n],gb)
        p[n]=self.displace(v[n],p[n])
        pener= model.evaluate(p[n])
        lener= model.evaluate(lb[n])        
        if(pener<lener):
          lb[n] = p[n]          
          if(pener < model.evaluate(gb)):
            gb = p[n]
      eb = model.evaluate(gb)
    return 0,eb,model


def wait():
  import time 
  time.sleep(1)


class Seive(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)
  

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10  

  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)

  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)

  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)

  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100

  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101

  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1

  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99

  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 

  import collections
  compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

  def energy(self,m,xblock,yblock,dictionary):
    def median(lst,ordered=False):
      if not ordered: lst= sorted(lst)
      n = len(lst)
      p = n//2
      if n % 2: return lst[p]
      q = p - 1
      q = max(0,min(q,n))
      return (lst[p] + lst[q])/2

    def stats(listl):
      from scipy.stats import scoreatpercentile
      q1 = scoreatpercentile(listl,25)
      q3 = scoreatpercentile(listl,75)  
      #print "IQR : %f"%(q3-q1)
      #print "Median: %f"%median(listl)
      return median(listl),(q3-q1)

    
    tempIndex=int(100*xblock+yblock)
    #print "energy| xblock: %d yblock: %d"%(xblock,yblock)
    #print "energy| TempIndex: " ,tempIndex
    energy=[]
    try:
      sample_no = int(myoptions['Seive']['subsample'])
      samples = random.sample(dictionary[tempIndex],sample_no)
      #print samples
      for x in samples:
        #if x.obj == [None]*len(objectives(m)):  evalscores+=1
        
       # print "before energy|x.changed: ",x.scores
        x.scores = score(m,x)
        x.changed = False
        #print "after energy|x.changed: ",x.scores,x.changed
        #print "ENERGY| score:",x.obj
        energy.append(x.scores)      
      median,iqr=stats(energy)
      return median,iqr
    except: return 0,0
      #print "Energy Error"
      #import traceback
      #traceback.print_exc()


  """
  Return a list of neighbours:
  """
  def listofneighbours(self,m,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL


  def searcher(self,m,dictionary):
    def randomC(): 
      return int(1+random.random()*7)
    def randomcell(): 
      return [randomC() for _ in xrange(2)]

    tries=0
    bmean,biqr,lbmean,lbiqr=1e6,1e6,1e6,1e6
    bsoln=[-1,-1]
    lives=int(myoptions['Seive']['lives'])
    while(tries<int(myoptions['Seive']['tries']) and  lives >= 0):
      #print "------------------Tries: %d-------------------"%lives
      #print tries<myoptions['Seive']['tries']
      soln = randomcell()
      tries+=1
      repeat=0
      #print "myoptions['Seive']['repeat']: ",myoptions['Seive']['repeat']
      #print "myoptions['Seive']['tries']: ",myoptions['Seive']['tries']
      #wait()
      while(repeat<int(myoptions['Seive']['repeat']) ):
        #print "Solution being tried: %d %d "%(soln[0],soln[1])
        result = self.generateNew(m,soln[0],soln[1],dictionary)
        if(result == False): 
          print "In middle of the desert"
          break
        else:
          #print "Searcher| Solution being tried: %d %d "%(soln[0],soln[1])
          smean,siqr = self.energy(m,soln[0],soln[1],dictionary)
          #print "Searcher| smean,siqr: %d %d "%(smean,siqr)
          neighbours = self.listofneighbours(m,soln[0],soln[1])
          #print neighbours
          nmean,niqr=1e6,1e6 
          for neighbour in neighbours:
            #print "Searcher| neighbour: ",neighbour
            result = self.generateNew(m,int(neighbour/100),neighbour%10,dictionary)
            #print "Searcher| points 
            if(result == True):
              tmean,tiqr = self.energy(m,int(neighbour/100),neighbour%10,dictionary)
              #print "Searcher| tmean,tiqr: ",tmean,tiqr
              if(tmean<nmean or (tmean==nmean and tiqr < niqr)):
                #print "Searcher| tmean: %f mean: %f"%(tmean,mean)
                #print "Searcher| tiqr: %f iqr: %f"%(tiqr,iqr)
                nsoln = [int(neighbour/100),neighbour%10]
                #print "Searcher|btsoln: ",btsoln
                nmean=tmean
                niqr=tiqr
            else:
              print "Searcher|NAAAAAAAAAAAAH"
              pass
          if(nmean<smean or (nmean == smean and nmean<smean)):
            soln=nsoln
            repeat+=1
          else:
            break
          

          #print nmean,smean,bmean,siqr,biqr
          if(min(nmean,smean)<bmean or (min(nmean,smean) == bmean and min(niqr,siqr)<biqr)):
            bmean=min(nmean,smean)
            biqr=min(niqr,siqr)
            if(nmean<smean or (nmean == smean and niqr<siqr)):
              bsoln=nsoln
            else: bsoln=soln
      if(bmean<lbmean or biqr <lbiqr): pass
      else:
        #print "Lost Life" 
        lives-=1
      lbmean=bmean
      lbiqr=biqr
#I need to look at slope now. The number of evaluation is not reducing a lot
#need to put a visited sign somewhere to stop evaluations 


    #print ">>>>>>>>>>>>>>WOW Mean:%f IQR: %f"%(bmean,biqr)
    #print ">>>>>>>>>>>>>>WOW Soultion: ",bsoln
    if(bsoln[0]==-1 and bsoln[1]==-1): raise Exception("No best solution found!")
    return bsoln

  def one(self,m,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def generateNew(self,m,xblock,yblock,dictionary):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|listInter: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))
          #print "generateNew| Decisions Length: ",len(decisions)
        #print "generateNew| Decisions: ",decisions
        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808

),"Something's wrong!" 
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808

),"Something's wrong!"
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False #A lot of points but right in the middle of a deseart
      else:
        return True
    """
    print interpolateCheck(xblock,yblock)
    """
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      temp = interpolate(x[0],x[1])
      decision.append(temp)
      count+=1
    
    return decision


  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint


  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum
  
  def decisions_check(self,dictionary):
    for i in dictionary.keys():
      for i in dictionary[i]:
        print " ",i.scores,
      print 


  def evaluate(self):
    def generate_dictionary():  
      dictionary = {}
      chess_board = whereMain(self.model) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def find_best_score(index,dictionary):
      mint=10e6
      for x in dictionary[self.convert(index[0],index[1])]:
        #print x.scores
        if(x.scores<mint): 
          mint=x.scores
          return_value = x
      return return_value

    model=self.model
    #print "Model used: %s"%(model.info())
    
    minR = model.minR
    maxR = model.maxR
    #model.baseline(minR,maxR)
    
    dictionary = generate_dictionary()
    bestSolution = self.searcher(self.model,dictionary)
    bestSolution = find_best_score(bestSolution,dictionary)
    #self.decisions_check(dictionary)
    #print "Number of points: ",self._checkDictionary(dictionary)
    return bestSolution.dec,bestSolution.scores,model

   

class Baseline(SearchersBasic):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS

  def evaluate(self,points=[],depth=0):
    def lo(m,x)      : return m.minR[x]
    def hi(m,x)      : return  m.maxR[x]
    def some(m,x):
      return lo(m,x) + random.random()*(hi(m,x) - lo(m,x))

    s = [] 
    m = self.model
    for _ in xrange(1000):
      tempSoln = [some(m,d) for d in xrange(m.n)]
      scre = m.evaluate(tempSoln)[-1]
      s.append(scre)
    return s

class Seive3(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive3']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive3']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive3']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,lz,cr=0.3,fmin=0.1,fmax=0.5):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z=lx[i],ly[i],lz[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint
    print "This was called######################################################"
    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision
  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 
  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)
  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)
  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)
  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100
  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101
  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1
  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99
  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 
  def generateNew(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    if flag == True:
      if convert(xblock,yblock) in dictionary: pass
      else:
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!"
      decisions=[]
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        assert(len(listInter)%2==0),"listInter%2 not 0"
        for i in xrange(int(len(listInter)/2)):
          #print "FLAG is True!"
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
          listInter[(i*2)+1],1000,dictionary))
      #else:
        #print "generateNew| Interpolation failed"
      listExter = extrapolateCheck(xblock,yblock)
      #print "generateNew|Extrapolation Check: ",listInter
      if(len(listExter)!= 0):
        #print "generateNew| Extrapolation failed"
      #else:
        #print "FLAG is True!"
        for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
            listExter[(2*i)+1],1000,dictionary))
      old = len(dictionary[convert(xblock,yblock)])
      
      for decision in decisions:dictionary[convert(xblock,yblock)].\
      append(self.generateSlot(m,decision,xblock,yblock))
      new = len(dictionary[convert(xblock,yblock)])
      #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
      return True,dictionary   


    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
            decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))

        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True,dictionary
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        #print "generateNew|Extrapolation Check: ",listInter
        if(len(listExter)==0):
         # print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False,dictionary
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
              decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True,dictionary
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False,dictionary #A lot of points but right in the middle of a deseart
      else:
        return True,dictionary

  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            matrix[i-1][j-1] = 100
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        #print "%0.3f"%matrix[i-1][j-1],
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
      #print
    
    #print graph[8]
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print "Depth: ",depth,
    #print "Points: ",len(graph[maxi]),
    #print "Maxi: ",maxi
    #import time
    #time.sleep(3)
    for x in graph[maxi]:
       #print "The cell is: ",x," depth is: ",depth
       if depth == int(myoptions['Seive3']['depth']):
         for i in xrange(0,5):
           y = any(dictionary[x])
           #print y
           temp2 = score(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
             #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
             #print bsoln.dec

           #print temp2,high,bsoln.dec
           #print
       
       if(depth < int(myoptions['Seive3']['depth'])):
         #print "RECURSE"
         #print "Cell No: ",x,x/100,x%10
         #print "Before: ",len(dictionary[x])
         result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
         #print "After: ",len(dictionary[x])
         rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
         #print high,sc
         if sc < high:
           high = sc 
           bsoln = rsoln
           #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
           #print bsoln.dec

    #print bsoln.dec     W
    return bsoln,high,model

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum

class Seive2_TM(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)



  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision


  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint


  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 

  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)

  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)

  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)

  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100

  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101

  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1

  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99

  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 

  def generateNew(self,m,xblock,yblock,dictionary):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
    ##print "generateNew| convert: ",convert(xblock,yblock)
    ##print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    ##print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      ##print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      ##print "generateNew|listInter: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))
          ##print "generateNew| Decisions Length: ",len(decisions)
        ##print "generateNew| Decisions: ",decisions
        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        ##print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        ##print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True
      else:
        ##print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        if(len(listExter)==0):
          ##print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!"
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          ##print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          ##print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        ##print "generateNew| Lot of points but middle of a desert"
        return False #A lot of points but right in the middle of a deseart
      else:
        return True
    """
    print interpolateCheck(xblock,yblock)
    """
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = wheredemo(self.model,points) #checked: working well
      #print chess_board
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      #print dictionary.keys()
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print graph.keys()
    #print "Number of points: ",len(graph[maxi])
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return bsoln.dec,high,model

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  #new_interpolate
  def n_i(self,m,dictionary,index):

    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    genPoint=[]
    row = index/100
    col = index%10
    xpoints=self.getpoints(index,dictionary)
    two = self.one(m,xpoints)
    three = self.one(m,xpoints)
    four = self.one(m,xpoints) 
    
    assert(len(two)==len(three)),"Something's wrong!"
    
    for i in xrange(len(two)):
      x,y,z=two[i],three[i],four[i]
      new = trim(m,x+0.1*abs(z-y),i)
      genPoint.append(new)
    dictionary[index].append(self.generateSlot(m,genPoint,row,col))
    return genPoint
   

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum
class Seive2(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)



  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision
  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 

  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)

  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)

  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)

  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100

  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101

  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1

  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99

  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 

  def generateNew(self,m,xblock,yblock,dictionary):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    ##print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
    ##print "generateNew| convert: ",convert(xblock,yblock)
    ##print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    ##print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      ##print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      ##print "generateNew|listInter: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))
          ##print "generateNew| Decisions Length: ",len(decisions)
        ##print "generateNew| Decisions: ",decisions
        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        ##print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!"
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False #A lot of points but right in the middle of a deseart
      else:
        return True
    """
    print interpolateCheck(xblock,yblock)
    """
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      #print chess_board
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      #print dictionary.keys()
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print graph.keys()
    #print "Number of points: ",len(graph[maxi])
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return bsoln.dec,high,model

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  #new_interpolate
  def n_i(self,m,dictionary,index):

    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    genPoint=[]
    row = index/100
    col = index%10
    xpoints=self.getpoints(index,dictionary)
    two = self.one(m,xpoints)
    three = self.one(m,xpoints)
    four = self.one(m,xpoints) 
    
    assert(len(two)==len(three)),"Something's wrong!"
    
    for i in xrange(len(two)):
      x,y,z=two[i],three[i],four[i]
      new = trim(m,x+0.1*abs(z-y),i)
      genPoint.append(new)
    dictionary[index].append(self.generateSlot(m,genPoint,row,col))
    return genPoint
   

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum
class Seive24(Seive2):

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=16              #number of columns in the chess board
    self.nrow=16               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def evaluate(self,points=[],depth=4):
    def generate_dictionary(points=[],depth=4):  
      dictionary = {}
      chess_board = whereMain(self.model,points,depth) #checked: working well
      tmax = 2**depth+1
      for i in range(1,tmax):
        for j in range(1,tmax):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(2**depth)] for x in range(2**depth)]
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    print "Maxi: ",maxi
    print "Number of cells with : ",len(graph[maxi])
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return bsoln.dec,high,model
class Seive25(Seive2):

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=32              #number of columns in the chess board
    self.nrow=32               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def evaluate(self,points=[],depth=5):
    def generate_dictionary(points=[],depth=5):  
      dictionary = {}
      chess_board = whereMain(self.model,points,depth) #checked: working well
      tmax = 2**depth+1
      for i in range(1,tmax):
        for j in range(1,tmax):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(2**depth)] for x in range(2**depth)]
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    print "Maxi: ",maxi
    print "Number of cells with : ",len(graph[maxi])
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return bsoln.dec,high,model
class Seive26(Seive2):

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=64              #number of columns in the chess board
    self.nrow=64               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def evaluate(self,points=[],depth=6):
    def generate_dictionary(points=[],depth=6):  
      dictionary = {}
      chess_board = whereMain(self.model,points,depth) #checked: working well
      tmax = 2**depth+1
      for i in range(1,tmax):
        for j in range(1,tmax):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(2**depth)] for x in range(2**depth)]
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,(2**depth)+1):
      for j in xrange(1,(2**depth)+1):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    print "Maxi: ",maxi
    print "Number of cells with : ",len(graph[maxi])
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return bsoln.dec,high,model
class Seive4(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)



  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision


  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint


  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 

  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)

  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)

  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)

  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100

  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101

  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1

  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99

  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 

  def generateNew(self,m,xblock,yblock,dictionary):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|listInter: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))
          #print "generateNew| Decisions Length: ",len(decisions)
        #print "generateNew| Decisions: ",decisions
        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!"
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False #A lot of points but right in the middle of a deseart
      else:
        return True
    """
    print interpolateCheck(xblock,yblock)
    """
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def evaluate(self,points=[],depth=0,repeat=100,f=0.75,cf=1):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print graph.keys()
    #print "Number of points: ",len(graph[maxi])
    count = 0
    #print "Number of islands: ",len(graph[maxi])
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       frontier = dictionary[x][:]
       if len(frontier) < 10: 
         #print "Before: ",len(frontier)
         for _ in xrange(20):
           frontier.append(self.n_i(model,frontier,x))
         #print "After: ",len(frontier)
       solution,minE = self.run_de(model,f,cf,frontier,x/100,x%10)
       if minE < high:
         high = minE
         bsoln = solution
    #print count     
    return bsoln.dec,high,model

  def threeOthers(self,frontier,one):
    #print "threeOthers"
    seen = [one]
    def other():
      #print "other"
      for i in xrange(len(frontier)):
        while True:
          k = random.randint(0,len(frontier)-1)
          #print "%d"%k
          if frontier[k] not in seen:
            seen.append(frontier[k])
            break
        return frontier[k]
    this = other()
    that = other()
    then = other()
    return this,that,then
  
  def trim(self,x,i)  : # trim to legal range
    m=self.model
    return max(m.minR[i], min(x, m.maxR[i]))      

  def extrapolate(self,model,frontier,one,f,cf,xb,yb):
    #print "Extrapolate"
    
    two,three,four = self.threeOthers(frontier,one)
    #print two,three,four
    solution=[]
    for d in xrange(self.model.n):
      x,y,z=two.dec[d],three.dec[d],four.dec[d]
      if(random.random() < cf):
        print cf
        solution.append(self.trim(x + f*(y-z),d))
      else:
        solution.append(one.dec[d]) 
    #print "blah"
    import sys
    sys.stdout.flush()
    return self.generateSlot(model,solution,xb,yb)

  def run_de(self,model,f,cf,frontier,xb,yb,repeat=100):
    def better(old,new):
      assert(len(old)==len(new)),"MOEAD| Length mismatch"
      for i in xrange(len(old)-1): #Since the score is return as [values of all objectives and energy at the end]
        if old[i] >= new[i]: continue
        else: return False
      return True
          
    def de(model,c,cf,frontier,xb,yb):
      model=self.model
      newF = []
      total,n=0,0
      for x in frontier:
        #print "update: %d"%n
        s = score(model,x)
        new = self.extrapolate(model,frontier,x,f,cf,xb,yb)
        #print new
        newe=score(model,new)
        if better(s,newe) == True:
          newF.append(new)
          n+=1
        else:
          newF.append(x)
        
      return newF,n  
    #print repeat
    lives = int(myoptions['Seive']['lives'])
    for indez in xrange(repeat):
      #print ".",
      frontier,n = de(model,f,cf,frontier,xb,yb)
      if n == 0: 
        print "Early Stop: ",indez,lives
        lives -= 1
        if lives == 0: break
    minR=9e10
    for x in frontier:
      #print x
      energy = score(model,x)[-1]
      if(minR>energy):
        minR = energy
        solution=x 
    return solution,minR 

    minR=9e10
    for x in frontier:
      #print x
      energy = score(model,x)[-1]
      if(minR>energy):
        minR = energy
        solution=x 
    return solution,minR    

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def getpoints_test(self,frontier):
    tempL = []
    #print frontier
    for x in frontier:
      tempL.append(x.dec)
    return tempL

  #new_interpolate
  def n_i(self,m,frontier,index):

    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    genPoint=[]
    row = index/100
    col = index%10
    xpoints=self.getpoints_test(frontier)
    two = self.one(m,xpoints)
    three = self.one(m,xpoints)
    four = self.one(m,xpoints) 
    
    assert(len(two)==len(three)),"Something's wrong!"
    
    for i in xrange(len(two)):
      x,y,z=two[i],three[i],four[i]
      new = trim(m,x+0.1*abs(z-y),i)
      genPoint.append(new)
    #frontier.append(self.generateSlot(m,genPoint,row,col))
    return self.generateSlot(m,genPoint,row,col)
   

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum
class Seive5(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0
  random.seed(1)



  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision


  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint


  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold =1#int(myoptions['Seive']['threshold'])         #threshold for number of points to be considered as a prospective solution
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 

  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)

  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)

  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)

  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100

  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101

  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1

  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99

  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 

  def generateNew(self,m,xblock,yblock,dictionary):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|listInter: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))
          #print "generateNew| Decisions Length: ",len(decisions)
        #print "generateNew| Decisions: ",decisions
        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!"
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False #A lot of points but right in the middle of a deseart
      else:
        return True
    """
    print interpolateCheck(xblock,yblock)
    """
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]

  def evaluate(self,points=[],depth=0,repeat=100,f=0.75,cf=0.3):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def select_min(model,dictionary,index):
      minval = 1e9
      for _ in xrange(10):
         temp = score(model,self.one(model,dictionary[index]))[-1]
         if temp < minval: minval = temp
      return temp


    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = select_min(model, dictionary,((i*100)+j))

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print graph.keys()
    #print "Number of points: ",len(graph[maxi])
    count = 0
    #print "Number of islands: ",len(graph[maxi])
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       frontier = dictionary[x][:]
       if len(frontier) < 10: 
         #print "Before: ",len(frontier)
         for _ in xrange(20):
           frontier.append(self.n_i(model,frontier,x))
         #print "After: ",len(frontier)
       solution,minE = self.run_de(model,f,cf,frontier,x/100,x%10)
       if minE < high:
         high = minE
         bsoln = solution
    #print count     
    return bsoln.dec,high,model

  def threeOthers(self,frontier,one):
    #print "threeOthers"
    seen = [one]
    def other():
      #print "other"
      for i in xrange(len(frontier)):
        while True:
          k = random.randint(0,len(frontier)-1)
          #print "%d"%k
          if frontier[k] not in seen:
            seen.append(frontier[k])
            break
        return frontier[k]
    this = other()
    that = other()
    then = other()
    return this,that,then
  
  def trim(self,x,i)  : # trim to legal range
    m=self.model
    return max(m.minR[i], min(x, m.maxR[i]))      

  def extrapolate(self,model,frontier,one,f,cf,xb,yb):
    #print "Extrapolate"
    two,three,four = self.threeOthers(frontier,one)
    #print two,three,four
    solution=[]
    for d in xrange(self.model.n):
      x,y,z=two.dec[d],three.dec[d],four.dec[d]
      if(random.random() < cf):
        solution.append(self.trim(x + f*(y-z),d))
      else:
        solution.append(one.dec[d]) 
    #print "blah"
    import sys
    sys.stdout.flush()
    return self.generateSlot(model,solution,xb,yb)
  def run_de(self,model,f,cf,frontier,xb,yb,repeat=100):
    def better(old,new):
      assert(len(old)==len(new)),"MOEAD| Length mismatch"
      for i in xrange(len(old)-1): #Since the score is return as [values of all objectives and energy at the end]
        if old[i] >= new[i]: continue
        else: return False
      return True
          
    def de(model,c,cf,frontier,xb,yb):
      model=self.model
      newF = []
      total,n=0,0
      for x in frontier:
        #print "update: %d"%n
        s = score(model,x)
        new = self.extrapolate(model,frontier,x,f,cf,xb,yb)
        #print new
        newe=score(model,new)
        if better(s,newe) == True:
          newF.append(new)
        else:
          newF.append(x)
        n+=1
      return newF  
    #print repeat
    for _ in xrange(repeat):
      #print ".",
      frontier = de(model,f,cf,frontier,xb,yb)
    minR=9e10
    for x in frontier:
      #print x
      energy = score(model,x)[-1]
      if(minR>energy):
        minR = energy
        solution=x 
    return solution,minR    

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def getpoints_test(self,frontier):
    tempL = []
    #print frontier
    for x in frontier:
      tempL.append(x.dec)
    return tempL

  #new_interpolate
  def n_i(self,m,frontier,index):

    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    genPoint=[]
    row = index/100
    col = index%10
    xpoints=self.getpoints_test(frontier)
    two = self.one(m,xpoints)
    three = self.one(m,xpoints)
    four = self.one(m,xpoints) 
    
    assert(len(two)==len(three)),"Something's wrong!"
    
    for i in xrange(len(two)):
      x,y,z=two[i],three[i],four[i]
      new = trim(m,x+0.1*abs(z-y),i)
      genPoint.append(new)
    #frontier.append(self.generateSlot(m,genPoint,row,col))
    return self.generateSlot(m,genPoint,row,col)
   

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum
class MOEAD(Seive5):
  
  def evaluate(self,points=[],depth=0,repeat=100,f=0.75,cf=0.3):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>myoptions["MOEAD"]["threshold"]):return True
        else:return False
      except:
        return False
    def select_min(model,dictionary,index):
      minval = 1e9
      for _ in xrange(10):
         temp = score(model,self.one(model,dictionary[index]))[-1]
         if temp < minval: minval = temp
      return temp


    model = self.model
    minR = model.minR
    maxR = model.maxR

    dictionary = generate_dictionary(points)
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            print "in middle of desert"
            continue

        
    high = 1e6
    bsoln = None

    for i in xrange(1,9):
      for j in xrange(1,9):
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       frontier = dictionary[i*100+j][:]
       if len(frontier) < 10: 
         #print "Before: ",len(frontier)
         for _ in xrange(20):
           frontier.append(self.n_i(model,frontier,x))
         #print "After: ",len(frontier)
       solution,minE = self.run_de(model,f,cf,frontier,x/100,x%10)
       if minE < high:
         high = minE
         bsoln = solution
    #print count     
    return bsoln.dec,high,model
class Seive2MG(Seive2):
  def evaluate(self,depth=0,repeat=100,lives=10):
    minR = 1e6
    listL,high,model = self.evaluate_wrapper()
    for _ in xrange(repeat):
      #say("#")
      if(minR >= high): minR = high
      else: lives-=1
      if lives == 0: break
      listL,high,model = self.evaluate_wrapper(listL)
    return listL,high,model 

  def evaluate_wrapper(self,points=[]):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def dicttolist(dictionary):
      listL = []
      for key in dictionary.keys():
        for item in dictionary[key]:
          item.xblock = -1
          item.yblock = -1
          listL.append(item)
      return listL

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print "Depth: %d #points: %d"%(depth,self._checkDictionary(dictionary))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]
        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        

    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    count = 0
    for x in graph[maxi]:
       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
       if(len(dictionary[x]) < 15): [self.n_i(model,dictionary,x) for _ in xrange(20)]
       #print "Seive2MG:A Number of points in ",maxi," is: ",len(dictionary[x])
       for y in dictionary[x]:
         temp2 = score(model,y)[-1]
         count += 1
         if temp2 < high:
           high = temp2
           bsoln = y
    #print count     
    return dicttolist(dictionary),high,model
class Seive2_V50(Seive3):
  def generateSlot(self,m,decision=[],x=-1,y=-1):
    if len(decision) == 0: d = [some(m,d) for d in xrange(m.n)]
    else: d = decision[:]
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=x,
            y=y,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint


  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint

  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]
    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return easts
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return wests



  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

    dictionary = generate_dictionary(points)
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        #print "%0.3f"%matrix[i-1][j-1],
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
      #print
    
    #print graph[8]
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print "Depth: ",depth,
    #print "Points: ",len(graph[maxi]),
    #print "Maxi: ",maxi
    #import time
    #time.sleep(3)
    for x in graph[maxi]:
       #print "The cell is: ",x," depth is: ",depth
       if depth == int(myoptions['Seive2_V50']['depth']):
         for i in xrange(0,5):
           y = any(dictionary[x])
           #print y
           temp2 = score(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
             #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
             #print bsoln.dec

           #print temp2,high,bsoln.dec
           #print
       
       if(depth < int(myoptions['Seive2_V50']['depth'])):
         #print "RECURSE"
         #print "Cell No: ",x,x/100,x%10
         #print "Before: ",len(dictionary[x])
         #lst = []
         self.tgenerate(model,dictionary[x]) #TODO: I don't really know how this works
         #print "After: ",len(dictionary[x])
         #self.extermaxlimit = 10
         #self.intermaxlimit = 10
         #result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)

         #print "Length1: ",len(dictionary[x])
         lst = self.fastmap(model,dictionary[x])
         #print "Length2: ",len(lst)
         print lst
         rsoln,sc,model = self.evaluate(lst,depth+1)
         #print high,sc
         if sc < high:
           high = sc 
           bsoln = rsoln
           #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
           #print bsoln.dec

    #print bsoln.dec     W
    return bsoln,high,model


# Remove t_generate. This simply doesn't work. Need to have intercell interpolation or extrapolation
# Remove polate()
# Improvement on Seive2, by adding ranking mechnism while selecting mountains

class Seive3_I1(Seive3):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive3_I1']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive3_I1']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive3_I1']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0


  def generateSlot(self,m,decision=[],x=-1,y=-1):
    if len(decision) == 0: d = [some(m,d) for d in xrange(m.n)]
    else: d = decision[:]
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=x,
            y=y,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint

  def generateNew1(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def thresholdCheck(index):
      try:
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        print "BOOM: "
        return False
    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      #print returnList
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
      
    newpoints=[]
    #print "xblock: ",xblock," yblock: ",yblock
    if convert(xblock,yblock) in dictionary: pass
    else:
      assert(convert(xblock,yblock)>=101),"Something's wrong!" 
      assert(convert(xblock,yblock)<=808),"Something's wrong!"
    decisions=[]
    listInter=interpolateCheck(xblock,yblock)
    #print "generateNew|Interpolation Check: ",listInter
    if(len(listInter)!=0):
      assert(len(listInter)%2==0),"listInter%2 not 0"
      for i in xrange(int(len(listInter)/2)):
        #print "FLAG is True!"
        decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
        listInter[(i*2)+1],1000,dictionary))
    else:
      print "generateNew| Interpolation failed"
    listExter = extrapolateCheck(xblock,yblock)
    #print "generateNew|Extrapolation Check: ",listInter
    if(len(listExter)== 0):
      print "generateNew| Extrapolation failed"
    else:
      #print "FLAG is True!"
      for i in xrange(int(len(listExter)/2)):
        decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
        listExter[(2*i)+1],1000,dictionary))

    old = len(dictionary[convert(xblock,yblock)])
    
    for decision in decisions:dictionary[convert(xblock,yblock)].\
    append(self.generateSlot(m,decision,xblock,yblock))
    new = len(dictionary[convert(xblock,yblock)])
    #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
    return True,dictionary   

  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      #print "Generate: ",len(points)
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",len(dictionary[index])
        if(len(dictionary[index]) >= self.threshold):return True
        else:return False
      except:
        return False

    def areneighbours(blocka,blockb):
      def overlap(a, b):
        return bool(set(a) & set(b))
      na = self.listofneighbours(int(blocka/100),blocka%10)
      nb = self.listofneighbours(int(blockb/100),blockb%10)
      return overlap(na,nb) 

    model = self.model
    minR = model.minR
    maxR = model.maxR
    ranking_dict = {}
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    dictionary = generate_dictionary(points)
    #print dictionary
    for indexzx in xrange(1):
      from collections import defaultdict
      graph = defaultdict(list)
      matrix = [[0 for x in range(8)] for x in range(8)]
      for i in xrange(1,9):
        for j in xrange(1,9):
          if(thresholdCheck(i*100+j,dictionary)==False):
            result,dictionary = self.generateNew(model,i,j,dictionary)
            if result == False: 
              matrix[i-1][j-1] = 100 #if no points can be generated then ignore
              #print "in middle of desert"
              continue
          matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

          
         # print matrix[i-1][j-1],
        #print
      for i in xrange(1,9):
        for j in xrange(1,9):
          sumn=0
          s = matrix[i-1][j-1]
          #print "%0.3f"%s,
          neigh = self.listofneighbours(i,j)
          sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
          #if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        #print
      
      #print "The graph in ",indexzx," is: ",graph[8]

      for ele in graph[8]:
        if ele in ranking_dict:
          ranking_dict[ele] += 1
        else:
          ranking_dict[ele] = 1
    
    #print ranking_dict
    max_value = max(ranking_dict.values())
    #print ">.................",max_value
    mountain =  [index for index in ranking_dict.keys() if ranking_dict[index] == max_value]
    #if there are more cells just pick 3 at random
    mountains = []
    if len(mountain) > int(myoptions['Seive3_I1']['subsample']): 
      mountains = [ any(mountain) for _ in xrange(3)]
    else:
      mountains = mountain[:]

    #print [len(dictionary[index]) for index in mountains]
    print mountains
    #raise Exception("I know python!")
    # for i in xrange(1,9):
    #   for j in xrange(1,9):
    #     try: print len(dictionary[i*100+j]),
    #     except: "emp",
    #   print 


    high = 1e6
    bsoln = None

    for x in mountains:
      if depth == int(myoptions['Seive3_I1']['depth']):
        for _ in xrange(1):
          y = any(dictionary[x])
          temp2 = score(model,y)[-1]
          if temp2 < high:
           high = temp2
           bsoln = y

      if(depth < int(myoptions['Seive3_I1']['depth'])):
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>AA>>>>>>>>>>>>>>>>>>"
        result,dictionary = self.generateNew1(model,int(x/100),x%10,dictionary)
        rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
        if sc < high:
          high = sc 
          bsoln = rsoln
      #raise Exception("I know python!")

    #print bsoln.dec     W
    return bsoln,high,model
    """This just doesn't make any differece"""

class Seive2_V50_1(Seive3):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive2_V50_1']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive2_V50_1']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive2_V50_1']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def tgenerate(self,m,pop,gen=0):
    if gen == 0:
      it = int(myoptions['Seive2_V50_1']['tgen'])
    else:
      it = gen
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand)
      #print one.dec
      pop += [one]
    return pop

  def generateSlot(self,m,decision=[],x=-1,y=-1):
    if len(decision) == 0: d = [some(m,d) for d in xrange(m.n)]
    else: d = decision[:]
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=x,
            y=y,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule
  def mutate(self,model,data):
    out = []
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)

    if score(model,west)[-1] < score(model,east)[-1]:
      east,west = west,east

    for point in data:
      out += [self.mutate1(model,point,c,east,west)]   
    
    #print len(data),len(out)
    data += out
   
    #assert(Before > After),"ouch"
    return data

  def lo(self,m,x)      : return m.minR[x]
  def hi(self,m,x)      : return  m.maxR[x]

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        print m.minR[x] , val.dec[x] , m.maxR[x]
        return False
    return True

  def mutate1(self,model,point,c,east,west,multiplier = 3.0):
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    #print "Distance: ",abs(newDistance)
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      print "Blown away"
      return point
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length: ", len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]

    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return easts
    else:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return wests

  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,lz,cr=0.9,fmin=0.1,fmax=0.5):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z=lx[i],ly[i],lz[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint
    #print "This was called######################################################"
    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count = 0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = interpolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision

  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.9,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision



  def generateNew(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10
    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False
    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList
    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "Number of cells: ",len(dictionary.keys())
    if flag == True:
      if convert(xblock,yblock) in dictionary: pass
      else:
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!"
      decisions=[]
      listInter=interpolateCheck(xblock,yblock)
      print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        assert(len(listInter)%2==0),"listInter%2 not 0"
        for i in xrange(int(len(listInter)/2)):
          #print "FLAG is True!"
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
          listInter[(i*2)+1],1000,dictionary))
      else:
        print "generateNew| Interpolation failed"
      listExter = extrapolateCheck(xblock,yblock)
      #print "generateNew|Extrapolation Check: ",listInter
      if(len(listExter)== 0):
        print "generateNew| Extrapolation failed"
      else:
        #print "FLAG is True!"
        decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
        listExter[(2*i)+1],1000,dictionary))
      old = len(dictionary[convert(xblock,yblock)])
      
      for decision in decisions:dictionary[convert(xblock,yblock)].\
      append(self.generateSlot(m,decision,xblock,yblock))
      new = len(dictionary[convert(xblock,yblock)])
      #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
      return True,dictionary   


    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False or thresholdCheck(convert(xblock,yblock))==True):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
            decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))

        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True,dictionary
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        #print "generateNew|Extrapolation Check: ",listExter
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False,dictionary
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
              decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True,dictionary
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False,dictionary #A lot of points but right in the middle of a deseart
      else:
        return True,dictionary
  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]


  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index]) > self.threshold):return True
        else:return False
      except:
        return False

    def randomcell(dictionary):
      assert(len(dictionary.keys()) > 0),"Something's wrong here"
      while True:
        a = int(1 + (9-1)*random.random())
        b = int(1 + (9-1)*random.random())
        try:
          len(dictionary[a*100+b])
          break
        except: pass
      return dictionary[a*100+b]


    model = self.model
    minR = model.minR
    maxR = model.maxR
    # if len(points) != 0:
    #   print "before: ",len(points)
    #   points = self.tgenerate(model,points,500)
    #   print "after: ",len(points)

    dictionary = generate_dictionary(points)
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    #print "Number of cells: ",len(dictionary.keys())
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    tempcount = 0
    for i in xrange(1,9):
      for j in xrange(1,9):
        # try: 
        #   print "\t",len(dictionary[i*100+j]),
        #   tempcount += 1#len(dictionary[i*100+j])
        # except: print "e",
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            matrix[i-1][j-1] = 100
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]
      #print
    #print "Cells used: ",tempcount,dictionary.keys()
    # for i in xrange(1,9):
    #   for j in xrange(1,9):
    #     if matrix[i-1][j-1] != 100: print "there ",i,j
    #if len(points) != 0: assert(tempcount == len(points)),"Screw up detected! %d"%tempcount


    #print "Matrix: ",matrix
    import time
    #time.sleep(2)

    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)

    #print "Graph: ",graph
    #import time
    #time.sleep(1)

    high = 1e6
    bsoln = None
    maxi = 8#max(graph.keys())
    #print "Maxi: ",maxi
    #print "List: ",graph[maxi]
    for x in graph[maxi]:
       #print "The cell is: ",x," depth is: ",depth
       if depth == int(myoptions['Seive2_V50_1']['depth']) or len(dictionary[x]) <= 2:
         for i in xrange(3):
           y = any(dictionary[x])
           #print y
           temp2 = score(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
       elif(depth < int(myoptions['Seive2_V50_1']['depth'])):
         #print "Points: ",len(dictionary[x])
         #print len(dictionary[x])
         if len(dictionary[x]) >= 2:
           olz = len(dictionary[x])
           result,dictionary = self.generateNew(model,int(x/100),x%100,dictionary)
           #print result,
           #print "Points Generated: ",len(dictionary[x])-olz
           #print "Before fastmap: ",len(lst)
           
           #print "After fastmap: ",len(lst)
           
           lst = self.mutate(model,dictionary[x])
           #print "Points Generated: ", len(lst)-olz
           lst = self.fastmap(model,lst) 

         rsoln,sc,model = self.evaluate(lst,depth+1)
         if sc < high:
           high = sc 
           bsoln = rsoln
    return bsoln,high,model

class Seive2_V50_2(Seive3):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive2_V50_2']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive2_V50_2']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive2_V50_2']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def tgenerate(self,m,pop,gen=0):
    if gen == 0:
      it = int(myoptions['Seive2_V50_1']['tgen'])
    else:
      it = gen
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand)
      #print one.dec
      pop += [one]
    return pop

  def generateSlot(self,m,decision=[],x=-1,y=-1):
    if len(decision) == 0: d = [some(m,d) for d in xrange(m.n)]
    else: d = decision[:]
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=x,
            y=y,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule
  def mutate(self,model,data):
    out = []
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)

    if score(model,west)[-1] < score(model,east)[-1]:
      east,west = west,east

    for point in data:
      out += [self.mutate1(model,point,c,east,west)]   
    
    #print len(data),len(out)
    data += out
   
    #assert(Before > After),"ouch"
    return data

  def lo(self,m,x)      : return m.minR[x]
  def hi(self,m,x)      : return  m.maxR[x]

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        print m.minR[x] , val.dec[x] , m.maxR[x]
        return False
    return True

  def mutate1(self,model,point,c,east,west,multiplier = 3.0):
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    #print "Distance: ",abs(newDistance)
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      print "Blown away"
      return point
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length: ", len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]

    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return easts
    else:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return wests

  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,lz,cr=0.9,fmin=0.1,fmax=0.5):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z=lx[i],ly[i],lz[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint
    #print "This was called######################################################"
    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count = 0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = interpolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision

  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.9,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision



  def generateNew(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10
    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False
    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList
    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "Number of cells: ",len(dictionary.keys())
    if flag == True:
      if convert(xblock,yblock) in dictionary: pass
      else:
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!"
      decisions=[]
      listInter=interpolateCheck(xblock,yblock)
      print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        assert(len(listInter)%2==0),"listInter%2 not 0"
        for i in xrange(int(len(listInter)/2)):
          #print "FLAG is True!"
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
          listInter[(i*2)+1],1000,dictionary))
      else:
        print "generateNew| Interpolation failed"
      listExter = extrapolateCheck(xblock,yblock)
      #print "generateNew|Extrapolation Check: ",listInter
      if(len(listExter)== 0):
        print "generateNew| Extrapolation failed"
      else:
        #print "FLAG is True!"
        decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
        listExter[(2*i)+1],1000,dictionary))
      old = len(dictionary[convert(xblock,yblock)])
      
      for decision in decisions:dictionary[convert(xblock,yblock)].\
      append(self.generateSlot(m,decision,xblock,yblock))
      new = len(dictionary[convert(xblock,yblock)])
      #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
      return True,dictionary   


    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False or thresholdCheck(convert(xblock,yblock))==True):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
            decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))

        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True,dictionary
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        #print "generateNew|Extrapolation Check: ",listExter
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False,dictionary
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
              decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True,dictionary
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False,dictionary #A lot of points but right in the middle of a deseart
      else:
        return True,dictionary
  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]


  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index]) > self.threshold):return True
        else:return False
      except:
        return False

    def randomcell(dictionary):
      assert(len(dictionary.keys()) > 0),"Something's wrong here"
      while True:
        a = int(1 + (9-1)*random.random())
        b = int(1 + (9-1)*random.random())
        try:
          len(dictionary[a*100+b])
          break
        except: pass
      return dictionary[a*100+b]


    model = self.model
    minR = model.minR
    maxR = model.maxR
    # if len(points) != 0:
    #   print "before: ",len(points)
    #   points = self.tgenerate(model,points,500)
    #   print "after: ",len(points)

    dictionary = generate_dictionary(points)
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    #print "Number of cells: ",len(dictionary.keys())
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    tempcount = 0
    for i in xrange(1,9):
      for j in xrange(1,9):
        # try: 
        #   print "\t",len(dictionary[i*100+j]),
        #   tempcount += 1#len(dictionary[i*100+j])
        # except: print "e",
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            matrix[i-1][j-1] = 100
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]
      #print
    #print "Cells used: ",tempcount,dictionary.keys()
    # for i in xrange(1,9):
    #   for j in xrange(1,9):
    #     if matrix[i-1][j-1] != 100: print "there ",i,j
    #if len(points) != 0: assert(tempcount == len(points)),"Screw up detected! %d"%tempcount


    #print "Matrix: ",matrix
    import time
    #time.sleep(2)

    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)

    #print "Graph: ",graph
    #import time
    #time.sleep(1)

    high = 1e6
    bsoln = None
    maxi = 8#max(graph.keys())
    #print "Maxi: ",maxi
    #print "List: ",graph[maxi]
    for x in graph[maxi]:
       #print "The cell is: ",x," depth is: ",depth
       if depth == int(myoptions['Seive2_V50_2']['depth']) or len(dictionary[x]) <= 4:
         for i in xrange(3):
           y = any(dictionary[x])
           #print y
           temp2 = score(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
       elif(depth < int(myoptions['Seive2_V50_2']['depth'])):
         #print "Points: ",len(dictionary[x])
         #print len(dictionary[x])
         if len(dictionary[x]) >= 2:
           olz = len(dictionary[x])
           result,dictionary = self.generateNew(model,int(x/100),x%100,dictionary)
           #print result,
           #print "Points Generated: ",len(dictionary[x])-olz
           #print "Before fastmap: ",len(lst)
           
           #print "After fastmap: ",len(lst)
           
           lst = self.mutate(model,dictionary[x])
           #print "Points Generated: ", len(lst)-olz
           lst = self.fastmap(model,lst) + randomcell(dictionary)

         rsoln,sc,model = self.evaluate(lst,depth+1)
         if sc < high:
           high = sc 
           bsoln = rsoln
    return bsoln,high,model


class Seive2_V50_3(Seive3):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive2_V50_3']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive2_V50_3']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive2_V50_3']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0

  def tgenerate(self,m,pop,gen=0):
    if gen == 0:
      it = int(myoptions['Seive2_V50_1']['tgen'])
    else:
      it = gen
    ret = []
    if len(pop) == 0: return []
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      #if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand)
      #print one.dec
      ret += [one]
    return ret

  def generateSlot(self,m,decision=[],x=-1,y=-1):
    if len(decision) == 0: d = [some(m,d) for d in xrange(m.n)]
    else: d = decision[:]
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=x,
            y=y,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule
  def mutate(self,model,data):
    out = []
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)

    if score(model,west)[-1] < score(model,east)[-1]:
      east,west = west,east

    for point in data:
      out += [self.mutate1(model,point,c,east,west)]   
    
    #print len(data),len(out)
    #data += out
   
    #assert(Before > After),"ouch"
    return out

  def lo(self,m,x)      : return m.minR[x]
  def hi(self,m,x)      : return  m.maxR[x]

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        print m.minR[x] , val.dec[x] , m.maxR[x]
        return False
    return True

  def mutate1(self,model,point,c,east,west,multiplier = 3.0):
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    #print "Distance: ",abs(newDistance)
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      print "Blown away"
      return point
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length: ", len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]

    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return easts
    else:
      cut, wests, easts = (xsum/len(data)), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return wests

  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,lz,cr=0.9,fmin=0.1,fmax=0.5):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z=lx[i],ly[i],lz[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint
    #print "This was called######################################################"
    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count = 0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = interpolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision

  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.9,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision



  def generateNew(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10
    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False
    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList
    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    #print "Number of cells: ",len(dictionary.keys())
    if flag == True:
      if convert(xblock,yblock) in dictionary: pass
      else:
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!"
      decisions=[]
      listInter=interpolateCheck(xblock,yblock)
      print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        assert(len(listInter)%2==0),"listInter%2 not 0"
        for i in xrange(int(len(listInter)/2)):
          #print "FLAG is True!"
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
          listInter[(i*2)+1],1000,dictionary))
      else:
        print "generateNew| Interpolation failed"
      listExter = extrapolateCheck(xblock,yblock)
      #print "generateNew|Extrapolation Check: ",listInter
      if(len(listExter)== 0):
        print "generateNew| Extrapolation failed"
      else:
        #print "FLAG is True!"
        decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
        listExter[(2*i)+1],1000,dictionary))
      old = len(dictionary[convert(xblock,yblock)])
      
      for decision in decisions:dictionary[convert(xblock,yblock)].\
      append(self.generateSlot(m,decision,xblock,yblock))
      new = len(dictionary[convert(xblock,yblock)])
      #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
      return True,dictionary   


    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False or thresholdCheck(convert(xblock,yblock))==True):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
            decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))

        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True,dictionary
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        #print "generateNew|Extrapolation Check: ",listExter
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False,dictionary
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
              decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True,dictionary
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        #print "generateNew| Lot of points but middle of a desert"
        return False,dictionary #A lot of points but right in the middle of a deseart
      else:
        return True,dictionary
  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]


  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index]) > self.threshold):return True
        else:return False
      except:
        return False

    def randomcell(model,dictionary,avoid):
      ret = []
      for x in dictionary.keys():
        if x in avoid: continue
        ret.append(self.one(model,dictionary[x]))
      #print ret
      print "Length: ",len(ret)
      #raise Exception("I know python!")
      return ret


    model = self.model
    minR = model.minR
    maxR = model.maxR
    # if len(points) != 0:
    #   print "before: ",len(points)
    #   points = self.tgenerate(model,points,500)
    #   print "after: ",len(points)

    dictionary = generate_dictionary(points)
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    #print "Number of cells: ",len(dictionary.keys())
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    tempcount = 0
    for i in xrange(1,9):
      for j in xrange(1,9):
        # try: 
        #   print "\t",len(dictionary[i*100+j]),
        #   tempcount += 1#len(dictionary[i*100+j])
        # except: print "e",
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            #print "in middle of desert"
            matrix[i-1][j-1] = 100
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]
      #print
    #print "Cells used: ",tempcount,dictionary.keys()
    # for i in xrange(1,9):
    #   for j in xrange(1,9):
    #     if matrix[i-1][j-1] != 100: print "there ",i,j
    #if len(points) != 0: assert(tempcount == len(points)),"Screw up detected! %d"%tempcount


    #print "Matrix: ",matrix
    import time
    #time.sleep(2)

    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)

    #print "Graph: ",graph
    #import time
    #time.sleep(1)

    high = 1e6
    bsoln = None
    maxi = 8#max(graph.keys())
    #print "Maxi: ",maxi
    #print "List: ",graph[maxi]
    lst = []
    for x in graph[maxi]: lst += dictionary[x]
       #print "The cell is: ",x," depth is: ",depth
    if depth == int(myoptions['Seive2_V50_3']['depth']) or len(lst) <= 4:
       for i in xrange(int(len(lst)/10)):
         y = any(dictionary[x])
         #print y
         temp2 = score(model,y)[-1]
         if temp2 < high:
           high = temp2
           bsoln = y
    elif(depth < int(myoptions['Seive2_V50_3']['depth'])):
       #print "Points: ",len(dictionary[x])
       #print len(dictionary[x])
       if len(lst) >= 2:
         olz = len(lst)
         #result,dictionary = self.generateNew(model,int(x/100),x%100,dictionary)
         #print result,
         #print "Points Generated: ",len(dictionary[x])-olz
         #print "Before fastmap: ",len(lst)
         
         #print "After fastmap: ",len(lst)
         
         lst += randomcell(model,dictionary,graph[maxi])
         print "Len of lst: ",len(lst)
         lst += self.mutate(model,lst) 
         print "Points Generated: ", len(lst)-olz
         lst = self.fastmap(model,lst) 
         print "Points Used: ", len(lst)

       rsoln,sc,model = self.evaluate(lst,depth+1)
       if sc < high:
         high = sc 
         bsoln = rsoln
    return bsoln,high,model



class Seive6(SearchersBasic): #minimizing
  model = None
  minR=0
  maxR=0

  def __init__(self,modelName,displayS,bmin,bmax):
    self.model = modelName
    self.model.minVal = bmin
    self.model.maxVal = bmax
    self.displayStyle=displayS
    self.threshold = int(myoptions['Seive3']['threshold'])         
    self.ncol=8               #number of columns in the chess board
    self.nrow=8               #number of rows in the chess board
    self.intermaxlimit=int(myoptions['Seive3']['intermaxlimit'])     #Max number of points that can be created by interpolation
    self.extermaxlimit=int(myoptions['Seive3']['extermaxlimit'])     #Max number of points that can be created by extrapolation
    self.evalscores=0
  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,lz,cr=0.3,fmin=0.1,fmax=0.5):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z=lx[i],ly[i],lz[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y
        genPoint.append(new)
      return genPoint
    print "This was called######################################################"
    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision
  def generateSlot(self,m,decision,x,y):
    newpoint=Slots(changed = True,
            scores=1e6, 
            xblock=-1, #sam
            yblock=-1,  #sam
            x=-1,
            y=-1,
            obj = [None] * m.objf, #This needs to be removed. Not using it as of 11/10
            dec = [some(m,d) for d in xrange(m.n)])

    #scores(m,newpoint)
    #print "Decision: ",newpoint.dec
    #print "Objectives: ",newpoint.obj
    return newpoint
  #There are three points and I am trying to extrapolate. Need to pass two cell numbers
  def wrapperextrapolate(self,m,xindex,yindex,maxlimit,dictionary):
    def extrapolate(lx,ly,lz,cr=0.3,fmin=0.9,fmax=2):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      def indexConvert(index):
        return int(index/100),index%10
      assert(len(lx)==len(ly)==len(lz))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y,z = lx[i],ly[i],lz[i]
        rand = random.random()

        if rand < cr:
          probEx = fmin + (fmax-fmin)*random.random()
          new = trim(m,x + probEx*(y-z),i)
        else:
          new = y #Just assign a value for that decision
        genPoint.append(new)
      return genPoint

    decision=[]
    #TODO: need to put an assert saying checking whether extrapolation is actually possible
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      two = self.one(m,xpoints)
      index2,index3=0,0
      while(index2 == index3): #just making sure that the indexes are not the same
        index2=random.randint(0,len(ypoints)-1)
        index3=random.randint(0,len(ypoints)-1)

      three=ypoints[index2]
      four=ypoints[index3]
      temp = extrapolate(two,three,four)
      #decision.append(extrapolate(two,three,four))
      decision.append(temp)
      count+=1
    return decision
  def convert(self,x,y): return (x*100)+y
  def rowno(self,x): return int(x/100)
  def colmno(self,x): return x%10 
  def gonw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==1):return self.convert(nrow,ncol)#in the first coulumn and first row
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)-1,ncol)#in the first column
    else: return (x-101)
  def gow(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==1): return self.convert(self.rowno(x),ncol)
    else: return (x-1)
  def gosw(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==1): return self.convert(1,ncol)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)-1)
    elif(self.colmno(x)==1): return self.convert(self.rowno(x)+1,ncol)
    else: return (x+99)
  def gos(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow): return self.convert(1,self.colmno(x))
    else: return x+100
  def gose(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==nrow and self.colmno(x)==ncol): return self.convert(1,1)
    elif(self.rowno(x)==nrow): return self.convert(1,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)+1,1)
    else: return x+101
  def goe(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.colmno(x)==ncol): return self.convert(self.rowno(x),1)
    else: return x+1
  def gone(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1 and self.colmno(x)==ncol): return self.convert(nrow,1)
    elif(self.rowno(x)==1): return self.convert(nrow,self.colmno(x)+1)
    elif(self.colmno(x)==ncol): return self.convert(self.rowno(x)-1,1)
    else: return x-99
  def gon(self,x):
    nrow=self.nrow
    ncol=self.ncol
    if(self.rowno(x)==1): return self.convert(nrow,self.colmno(x))
    else: return x-100 
  def generateNew(self,m,xblock,yblock,dictionary,flag = False):
    convert = self.convert
    rowno = self.rowno
    colmno = self.colmno 

    def indexConvert(index):
      return int(index/100),index%10

    def opposite(a,b):
      ax,ay,bx,by=a/100,a%100,b/100,b%100
      if(abs(ax-bx)==2 or abs(ay-by)==2):return True
      else: return False

    def thresholdCheck(index):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False

    def interpolateCheck(xblock,yblock):
      returnList=[]
      if(thresholdCheck(self.gonw(convert(xblock,yblock))) and thresholdCheck(self.gose(convert(xblock,yblock))) == True):
        returnList.append(self.gonw(convert(xblock,yblock)))
        returnList.append(self.gose(convert(xblock,yblock)))
      if(thresholdCheck(self.gow(convert(xblock,yblock))) and thresholdCheck(self.goe(convert(xblock,yblock))) == True):
       returnList.append(self.gow(convert(xblock,yblock)))
       returnList.append(self.goe(convert(xblock,yblock)))
      if(thresholdCheck(self.gosw(convert(xblock,yblock))) and thresholdCheck(self.gone(convert(xblock,yblock))) == True):
       returnList.append(self.gosw(convert(xblock,yblock)))
       returnList.append(self.gone(convert(xblock,yblock)))
      if(thresholdCheck(self.gon(convert(xblock,yblock))) and thresholdCheck(self.gos(convert(xblock,yblock))) == True):
       returnList.append(self.gon(convert(xblock,yblock)))
       returnList.append(self.gos(convert(xblock,yblock)))
      return returnList


    def extrapolateCheck(xblock,yblock):
      #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
      #TODO: Need to make this logic more succint
      returnList=[]
      #go North West
      temp = self.gonw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gonw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gonw(temp))

      #go North 
      temp = self.gon(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gon(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gon(temp))

      #go North East
      temp = self.gone(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gone(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gone(temp))
  
      #go East
      temp = self.goe(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.goe(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.goe(temp))

      #go South East
      temp = self.gose(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gose(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gose(temp))

      #go South
      temp = self.gos(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gos(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gos(temp))

      #go South West
      temp = self.gosw(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gosw(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gosw(temp))
 
      #go West
      temp = self.gow(convert(xblock,yblock))
      result1 = thresholdCheck(temp)
      if result1 == True:
        result2 = thresholdCheck(self.gow(temp))
        if(result1 == True and result2 == True):
          returnList.append(temp)
          returnList.append(self.gow(temp))

      return returnList
  
    newpoints=[]
    if flag == True:
      if convert(xblock,yblock) in dictionary: pass
      else:
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!"
      decisions=[]
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        assert(len(listInter)%2==0),"listInter%2 not 0"
        for i in xrange(int(len(listInter)/2)):
          #print "FLAG is True!"
          decisions.extend(self.wrapperInterpolate(m,listInter[i*2],\
          listInter[(i*2)+1],1000,dictionary))
      #else:
        #print "generateNew| Interpolation failed"
      listExter = extrapolateCheck(xblock,yblock)
      #print "generateNew|Extrapolation Check: ",listInter
      if(len(listExter)!= 0):
        #print "generateNew| Extrapolation failed"
      #else:
        #print "FLAG is True!"
        for i in xrange(int(len(listExter)/2)):
            decisions.extend(self.wrapperextrapolate(m,listExter[2*i],\
            listExter[(2*i)+1],1000,dictionary))
      old = len(dictionary[convert(xblock,yblock)])
      
      for decision in decisions:dictionary[convert(xblock,yblock)].\
      append(self.generateSlot(m,decision,xblock,yblock))
      new = len(dictionary[convert(xblock,yblock)])
      #print "generateNew|Flag:True| Number of new points generated: ", (new-old) 
      return True,dictionary   


    #print "generateNew| convert: ",convert(xblock,yblock)
    #print "generateNew| thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
    #print "generateNew| points in the block: ",len(dictionary[convert(xblock,yblock)])
    if(thresholdCheck(convert(xblock,yblock))==False):
      #print "generateNew| Cell is relatively sparse: Might need to generate new points"
      listInter=interpolateCheck(xblock,yblock)
      #print "generateNew|Interpolation Check: ",listInter
      if(len(listInter)!=0):
        decisions=[]
        assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
        for i in xrange(int(len(listInter)/2)):
            decisions.extend(self.wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(self.intermaxlimit/len(listInter))+1,dictionary))

        if convert(xblock,yblock) in dictionary: pass
        else:
          #print convert(xblock,yblock)
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!"
          dictionary[convert(xblock,yblock)]=[]
        old = self._checkDictionary(dictionary)
        for decision in decisions:dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
        #print "generateNew| Interpolation works!"
        new = self._checkDictionary(dictionary)
        #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
        return True,dictionary
      else:
        #print "generateNew| Interpolation failed!"
        decisions=[]
        listExter = extrapolateCheck(xblock,yblock)
        #print "generateNew|Extrapolation Check: ",listInter
        if(len(listExter)==0):
          #print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
          return False,dictionary
        else:
          assert(len(listExter)%2==0),"listExter%2 not 0"
          for i in xrange(int(len(listExter)/2)):
              decisions.extend(self.wrapperextrapolate(m,listExter[2*i],listExter[(2*i)+1],int(self.extermaxlimit)/len(listExter),dictionary))
          if convert(xblock,yblock) in dictionary: pass
          else: 
            assert(convert(xblock,yblock)>=101),"Something's wrong!" 
            #assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            assert(convert(xblock,yblock)<=808),"Something's wrong!" 
            dictionary[convert(xblock,yblock)]=[]
          old = self._checkDictionary(dictionary)
          for decision in decisions: dictionary[convert(xblock,yblock)].append(self.generateSlot(m,decision,xblock,yblock))
          new = self._checkDictionary(dictionary)
          #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
          #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
          return True,dictionary
    else:
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter) == 0):
        print "generateNew| Lot of points but middle of a desert"
        return False,dictionary #A lot of points but right in the middle of a deseart
      else:
        return True,dictionary

  def wrapperInterpolate(self,m,xindex,yindex,maxlimit,dictionary):
    def interpolate(lx,ly,cr=0.3,fmin=0,fmax=1):
      def lo(m,index)      : return m.minR[index]
      def hi(m,index)      : return m.maxR[index]
      def trim(m,x,i)  : # trim to legal range
        return max(lo(m,i), x%hi(m,i))
      assert(len(lx)==len(ly))
      genPoint=[]
      for i in xrange(len(lx)):
        x,y=lx[i],ly[i]
        #print x
        #print y
        rand = random.random
        if rand < cr:
          probEx = fmin +(fmax-fmin)*rand()
          new = trim(m,min(x,y)+probEx*abs(x-y),i)
        else:
          new = y 
        genPoint.append(new)
      return genPoint

    decision=[]
    #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
    #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
    xpoints=self.getpoints(xindex,dictionary)
    ypoints=self.getpoints(yindex,dictionary)
    import itertools
    listpoints=list(itertools.product(xpoints,ypoints))
    #print "Length of Listpoints: ",len(listpoints)
    count=0
    while True:
      if(count>min(len(xpoints),maxlimit)):break
      x=self.one(m,listpoints)
      decision.append(interpolate(x[0],x[1]))
      count+=1
    return decision



  def listofneighbours(self,xblock,yblock):
    index=self.convert(xblock,yblock)
    #print "listofneighbours| Index passed: ",index
    listL=[]
    listL.append(self.goe(index))
    listL.append(self.gose(index))
    listL.append(self.gos(index))
    listL.append(self.gosw(index))
    listL.append(self.gow(index))
    listL.append(self.gonw(index))
    listL.append(self.gon(index))
    listL.append(self.gone(index))
    return listL

  def getpoints(self,index,dictionary):
    tempL = []
    for x in dictionary[index]:tempL.append(x.dec)
    return tempL

  def sdiv(self,lst, tiny=3,cohen=0.3,
           num1=lambda x:x[0], num2=lambda x:x[1]):
    "Divide lst of (num1,num2) using variance of num2."
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
      lhs,rhs = Counts(), Counts(num2(x) for x in this)
      n0, least, cut = 1.0*rhs.n, rhs.sd(), None
      for j,x  in enumerate(this): 
        if lhs.n > tiny and rhs.n > tiny: 
          maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
          if maybe < least :  
            if abs(lhs.mu - rhs.mu) >= small: # where's the paper for this method?
              cut,least = j,maybe
        rhs - num2(x)
        lhs + num2(x)    
      return cut,least
    #----------------------------------------------
    def recurse(this, small,cuts):
      #print this,small
      cut,sd = divide(this,small)
      if cut: 
        recurse(this[:cut], small, cuts)
        recurse(this[cut:], small, cuts)
      else:   
        cuts += [(sd,this)]
      return cuts
    #---| main |-----------------------------------
    # for x in lst:
    #   print num2(x)
    small = Counts(num2(x) for x in lst).sd()*cohen # why we use a cohen??? how to choose cohen
    if lst: 
      return recurse(sorted(lst,key=num1),small,[])


  def one(self,model,lst): 
    def any(l,h):
      return (0 + random.random()*(h-l))
    return lst[int(any(0,len(lst) - 1)) ]
  
  def generate2(self,model,constraints):
    def any(l,h):
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(950):
      dec = []
      for constraint in constraints:
        lo,hi = self.one(model,constraint[1])
        # lo,hi = constraint[0],constraint[1]
        temp = any(lo,hi)
        assert(temp >= lo and temp <= hi),"ranges are messed up"
        dec.append(temp)
      points.append(self.generateSlot(model,dec,-1,-1))
      #print "\n\n",points
    assert(len(points) == 950),"all the points were not generated"
    return points


  def evaluate(self,points=[],depth=0):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",self.threshold
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def indexof(lsts,number,index = lambda x: x[1]):
      for i,lst in enumerate(sorted(lsts,key = index)):
        if number == index(lst): return i
      return -1 
    def uscore(lsts,starti,endi):
      summ = 0
      for i in xrange(starti,endi+1):
        summ += lsts[i][-1]
      return summ/(endi-starti+1)

    model = self.model
    minR = model.minR
    maxR = model.maxR
    if depth == 0 and len(points) == 0: 
      #generate points according to the constraints
      points = return_points(model,50)
      for point in points:
        point.score = score(model,point)[-1]
      
      points = [point.dec+[point.score] for point in points]
      constraints = []
      for i in xrange(len(points[0])-1):
        constraint = []
        cohen=0.6
        h = 1e6
        #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
        # print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
        for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
        #   starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
        #   endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
        #   print "Starti: ",starti, "Endi: ",endi
        #   mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
        #   #print "-----------------Mean Score: ",mean_score
        #   if mean_score < h:
        #     const1 = d[1][0][i]
        #     const2 = d[1][-1][i]
        #     h = mean_score
        #     print "+++++++++++++++High Mean Score: ",h
           constraint.append((d[1][0][i],d[1][-1][i]))
        constraints.append([i]+[constraint])# (const1,const2)])  
      #raise Exception(":asd")    
      points = self.generate2(model,constraints)
      #print "SDIV working!"

    dictionary = generate_dictionary(points)
    # for key in dictionary.keys():
    #   if len(dictionary[key]) == 0: print ">>>>>>>>>>>>>>>>>>>>>>>"
    #   print "Key: ",key," Length: ",len(dictionary[key])
    # raise Exception("asdaskdj")

    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9):
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(model,i,j,dictionary)
          if result == False: 
            matrix[i-1][j-1] = 100
            #print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        #print "%0.3f"%matrix[i-1][j-1],
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
      #print
    
    #print graph[8]
    high = 1e6
    bsoln = None
    maxi = max(graph.keys())
    #print "Depth: ",depth,
    #print "Points: ",len(graph[maxi]),
    #print "Maxi: ",maxi
    #import time
    #time.sleep(3)
    for x in graph[maxi]:
       #print "The cell is: ",x," depth is: ",depth
       if depth == int(myoptions['Seive3']['depth']):
         for i in xrange(0,5):
           y = any(dictionary[x])
           #print y
           temp2 = score(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
             #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
             #print bsoln.dec

           #print temp2,high,bsoln.dec
           #print
       
       if(depth < int(myoptions['Seive3']['depth'])):
         #print "RECURSE"
         #print "Cell No: ",x,x/100,x%10
         #print "Before: ",len(dictionary[x])
         result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
         #print "After: ",len(dictionary[x])
         rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
         #print high,sc
         if sc < high:
           high = sc 
           bsoln = rsoln
           #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
           #print bsoln.dec

    #print bsoln.dec     W
    return bsoln,high,model

  def _checkDictionary(self,dictionary):
    sum=0
    for i in dictionary.keys():
      sum+=len(dictionary[i])
    return sum

class Seive7(Seive6):
  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(950):
      dec = []
      for constraint in constraints:
        #lo,hi = self.one(model,constraint )
        #print constraint
        lo,hi = constraint[1][0],constraint[1][1]
        temp = any(lo,hi)
        assert(temp >= lo and temp <= hi),"ranges are messed up"
        dec.append(temp)
      points.append(self.generateSlot(model,dec,-1,-1))
      #print "\n\n",points
    assert(len(points) == 950),"all the points were not generated"
    return points
  def evaluate(self,points=[],depth=0):
      def generate_dictionary(points=[]):  
        dictionary = {}
        chess_board = whereMain(self.model,points) #checked: working well
        for i in range(1,9):
          for j in range(1,9):
            temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
            if(len(temp)!=0):
              index=temp[0].xblock*100+temp[0].yblock
              dictionary[index] = temp
              assert(len(temp)==len(dictionary[index])),"something"
        return dictionary

      def thresholdCheck(index,dictionary):
        try:
          #print "Threshold Check: ",self.threshold
          if(len(dictionary[index])>self.threshold):return True
          else:return False
        except:
          return False
      def indexof(lsts,number,index = lambda x: x[1]):
        for i,lst in enumerate(sorted(lsts,key = index)):   
          if number == index(lst): return i
        return -1 
      def uscore(lsts,starti,endi):
        summ = 0
        for i in xrange(starti,endi+1):
          summ += lsts[i][-1]
        return summ/(endi-starti+1)

      model = self.model
      minR = model.minR
      maxR = model.maxR
      if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
        points = return_points(model,50)
        for point in points:
          point.score = score(model,point)[-1]
        
        points = [point.dec+[point.score] for point in points]
        constraints = []
        for i in xrange(len(points[0])-1):
          constraint = []
          cohen=0.6
          h = 1e6
          #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
          #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
          for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
            starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
            endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
            #print "Starti: ",starti, "Endi: ",endi
            mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
            #print "-----------------Mean Score: ",mean_score
            if mean_score < h:
              const1 = d[1][0][i]
              const2 = d[1][-1][i]
              h = mean_score
              #print "+++++++++++++++High Mean Score: ",h
          #constraint.append()

          
          constraints.append([i]+[(const1,const2)])  
        # print constraints
        # raise Exception(":asd")    
        points = self.generate2(model,constraints)
        #print "SDIV working!"

      dictionary = generate_dictionary(points)
      # for key in dictionary.keys():
      #   if len(dictionary[key]) == 0: print ">>>>>>>>>>>>>>>>>>>>>>>"
      #   print "Key: ",key," Length: ",len(dictionary[key])
      # raise Exception("asdaskdj")

      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
      from collections import defaultdict
      graph = defaultdict(list)
      matrix = [[0 for x in range(8)] for x in range(8)]
      for i in xrange(1,9):
        for j in xrange(1,9):
          if(thresholdCheck(i*100+j,dictionary)==False):
            result,dictionary = self.generateNew(model,i,j,dictionary)
            if result == False: 
              matrix[i-1][j-1] = 100
              #print "in middle of desert"
              continue
          matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

          
         # print matrix[i-1][j-1],
        #print
      for i in xrange(1,9):
        for j in xrange(1,9):
          #print "%0.3f"%matrix[i-1][j-1],
          sumn=0
          s = matrix[i-1][j-1]
          neigh = self.listofneighbours(i,j)
          sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
          if (i*100+j) in dictionary:
            graph[int(sumn)].append(i*100+j)
        #print
      
      #print graph[8]
      high = 1e6
      bsoln = None
      maxi = max(graph.keys())
      #print "Depth: ",depth,
      #print "Points: ",len(graph[maxi]),
      #print "Maxi: ",maxi
      #import time
      #time.sleep(3)
      for x in graph[maxi]:
         #print "The cell is: ",x," depth is: ",depth
         if depth == int(myoptions['Seive3']['depth']):
           for i in xrange(0,5):
             y = any(dictionary[x])
             #print y
             temp2 = score(model,y)[-1]
             if temp2 < high:
               high = temp2
               bsoln = y
               #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
               #print bsoln.dec

             #print temp2,high,bsoln.dec
             #print
         
         if(depth < int(myoptions['Seive3']['depth'])):
           #print "RECURSE"
           #print "Cell No: ",x,x/100,x%10
           #print "Before: ",len(dictionary[x])
           result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
           #print "After: ",len(dictionary[x])
           rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
           #print high,sc
           if sc < high:
             high = sc 
             bsoln = rsoln
             #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
             #print bsoln.dec

      #print bsoln.dec     W
      return bsoln,high,model
class Seive7_1(Seive7):
  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(940):
      dec = []
      for constraint in constraints:
        #lo,hi = self.one(model,constraint )
        #print constraint
        lo,hi = constraint[1][0],constraint[1][1]
        temp = any(lo,hi)
        assert(temp >= lo and temp <= hi),"ranges are messed up"
        dec.append(temp)
      points.append(self.generateSlot(model,dec,-1,-1))
      #print "\n\n",points
    assert(len(points) == 940),"all the points were not generated"
    return points

  def evaluate(self,points=[],depth=0):
      def generate_dictionary(points=[]):  
        dictionary = {}
        chess_board = whereMain(self.model,points) #checked: working well
        for i in range(1,9):
          for j in range(1,9):
            temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
            if(len(temp)!=0):
              index=temp[0].xblock*100+temp[0].yblock
              dictionary[index] = temp
              assert(len(temp)==len(dictionary[index])),"something"
        return dictionary

      def thresholdCheck(index,dictionary):
        try:
          #print "Threshold Check: ",self.threshold
          if(len(dictionary[index])>self.threshold):return True
          else:return False
        except:
          return False
      def indexof(lsts,number,index = lambda x: x[1]):
        for i,lst in enumerate(sorted(lsts,key = index)):   
          if number == index(lst): return i
        return -1 
      def uscore(lsts,starti,endi):
        summ = 0
        for i in xrange(starti,endi+1):
          summ += lsts[i][-1]
        return summ/(endi-starti+1)

      model = self.model
      minR = model.minR
      maxR = model.maxR
      if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
        points = return_points(model,60)
        for point in points:
          point.score = score(model,point)[-1]
        
        points = [point.dec+[point.score] for point in points]
        constraints = []
        for i in xrange(len(points[0])-1):
          constraint = []
          cohen=0.3
          h = 1e6
          #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
          #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
          for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
            starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
            endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
            #print "Starti: ",starti, "Endi: ",endi
            mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
            #print "-----------------Mean Score: ",mean_score
            if mean_score < h:
              const1 = d[1][0][i]
              const2 = d[1][-1][i]
              h = mean_score
              #print "+++++++++++++++High Mean Score: ",h
          #constraint.append()

          
          constraints.append([i]+[(const1,const2)])  
        # print constraints
        # raise Exception(":asd")    
        points = self.generate2(model,constraints)
        #print "SDIV working!"

      dictionary = generate_dictionary(points)
      # for key in dictionary.keys():
      #   if len(dictionary[key]) == 0: print ">>>>>>>>>>>>>>>>>>>>>>>"
      #   print "Key: ",key," Length: ",len(dictionary[key])
      # raise Exception("asdaskdj")

      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
      from collections import defaultdict
      graph = defaultdict(list)
      matrix = [[0 for x in range(8)] for x in range(8)]
      for i in xrange(1,9):
        for j in xrange(1,9):
          if(thresholdCheck(i*100+j,dictionary)==False):
            result,dictionary = self.generateNew(model,i,j,dictionary)
            if result == False: 
              matrix[i-1][j-1] = 100
              #print "in middle of desert"
              continue
          matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

          
         # print matrix[i-1][j-1],
        #print
      for i in xrange(1,9):
        for j in xrange(1,9):
          #print "%0.3f"%matrix[i-1][j-1],
          sumn=0
          s = matrix[i-1][j-1]
          neigh = self.listofneighbours(i,j)
          sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
          if (i*100+j) in dictionary:
            graph[int(sumn)].append(i*100+j)
        #print
      
      #print graph[8]
      high = 1e6
      bsoln = None
      maxi = max(graph.keys())
      #print "Depth: ",depth,
      #print "Points: ",len(graph[maxi]),
      #print "Maxi: ",maxi
      #import time
      #time.sleep(3)
      for x in graph[maxi]:
         #print "The cell is: ",x," depth is: ",depth
         if depth == int(myoptions['Seive3']['depth']):
           for i in xrange(0,5):
             y = any(dictionary[x])
             #print y
             temp2 = score(model,y)[-1]
             if temp2 < high:
               high = temp2
               bsoln = y
               #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
               #print bsoln.dec

             #print temp2,high,bsoln.dec
             #print
         
         if(depth < int(myoptions['Seive3']['depth'])):
           #print "RECURSE"
           #print "Cell No: ",x,x/100,x%10
           #print "Before: ",len(dictionary[x])
           result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
           #print "After: ",len(dictionary[x])
           rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
           #print high,sc
           if sc < high:
             high = sc 
             bsoln = rsoln
             #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
             #print bsoln.dec

      #print bsoln.dec     W
      return bsoln,high,model


class Seive7_2(Seive7):
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length of data: ",len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]
    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return easts
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      return wests

  def tgenerate(self,m,pop,gen=0):
    it = int(myoptions['Seive7_2']['tgen'])
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand,-1,-1)
      #print one.dec
      pop += [one]
    return pop

  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      return max(lo(m,i), x%hi(m,i))
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint


  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(20):
      for _ in xrange(200):
        dec = []
        for constraint in constraints:
          #lo,hi = self.one(model,constraint )
          #print constraint
          lo,hi = constraint[1][0],constraint[1][1]
          temp = any(lo,hi)
          assert(temp >= lo and temp <= hi),"ranges are messed up"
          dec.append(temp)
        points.append(self.generateSlot(model,dec,-1,-1))
      #print "After Generation: ",len(points)
      points = self.fastmap(model,points)
      #print "After FastMap: ",len(points)
      points = self.tgenerate(model,points)
    #print ">>>>>>>Final: ",len(points)
    #raise Exception("asdasdasffd")
    #print "\n\n",points
    #assert(len(points) == 940),"all the points were not generated"
    return points



  def evaluate(self,points=[],depth=0):
      def generate_dictionary(points=[]):  
        dictionary = {}
        chess_board = whereMain(self.model,points) #checked: working well
        for i in range(1,9):
          for j in range(1,9):
            temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
            if(len(temp)!=0):
              index=temp[0].xblock*100+temp[0].yblock
              dictionary[index] = temp
              assert(len(temp)==len(dictionary[index])),"something"
        return dictionary

      def thresholdCheck(index,dictionary):
        try:
          #print "Threshold Check: ",self.threshold
          if(len(dictionary[index])>self.threshold):return True
          else:return False
        except:
          return False
      def indexof(lsts,number,index = lambda x: x[1]):
        for i,lst in enumerate(sorted(lsts,key = index)):   
          if number == index(lst): return i
        return -1 
      def uscore(lsts,starti,endi):
        summ = 0
        for i in xrange(starti,endi+1):
          summ += lsts[i][-1]
        return summ/(endi-starti+1)

      model = self.model
      minR = model.minR
      maxR = model.maxR
      if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
        points = return_points(model,60)
        for point in points:
          point.score = score(model,point)[-1]
        
        points = [point.dec+[point.score] for point in points]
        constraints = []
        for i in xrange(len(points[0])-1):
          constraint = []
          cohen=0.3
          h = 1e6
          #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
          #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
          for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
            starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
            endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
            #print "Starti: ",starti, "Endi: ",endi
            mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
            #print "-----------------Mean Score: ",mean_score
            if mean_score < h:
              const1 = d[1][0][i]
              const2 = d[1][-1][i]
              h = mean_score
              #print "+++++++++++++++High Mean Score: ",h
          #constraint.append()

          
          constraints.append([i]+[(const1,const2)])  
        # print constraints
        # raise Exception(":asd")    
        points = self.generate2(model,constraints)


        #print "SDIV working!"
      #print "Initial Points: ",len(points)
      dictionary = generate_dictionary(points)
      # for key in dictionary.keys():
      #   if len(dictionary[key]) == 0: print ">>>>>>>>>>>>>>>>>>>>>>>"
      #   print "Key: ",key," Length: ",len(dictionary[key])
      # raise Exception("asdaskdj")

      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
      from collections import defaultdict
      graph = defaultdict(list)
      matrix = [[0 for x in range(8)] for x in range(8)]
      for i in xrange(1,9):
        for j in xrange(1,9):
          if(thresholdCheck(i*100+j,dictionary)==False):
            result,dictionary = self.generateNew(model,i,j,dictionary)
            if result == False: 
              matrix[i-1][j-1] = 100
              #print "in middle of desert"
              continue
          matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

          
         # print matrix[i-1][j-1],
        #print
      for i in xrange(1,9):
        for j in xrange(1,9):
          #print "%0.3f"%matrix[i-1][j-1],
          sumn=0
          s = matrix[i-1][j-1]
          neigh = self.listofneighbours(i,j)
          sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
          if (i*100+j) in dictionary:
            graph[int(sumn)].append(i*100+j)
        #print
      
      #print graph[8]
      high = 1e6
      bsoln = None
      maxi = max(graph.keys())
      #print "Depth: ",depth,
      #print "Points: ",len(graph[maxi]),
      #print "Maxi: ",maxi
      #import time
      #time.sleep(3)
      for x in graph[maxi]:
         #print "The cell is: ",x," depth is: ",depth
         if depth == int(myoptions['Seive3']['depth']):
           for i in xrange(0,5):
             y = any(dictionary[x])
             #print y
             temp2 = score(model,y)[-1]
             if temp2 < high:
               high = temp2
               bsoln = y
               #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
               #print bsoln.dec

             #print temp2,high,bsoln.dec
             #print
         
         if(depth < int(myoptions['Seive3']['depth'])):
           #print "RECURSE"
           #print "Cell No: ",x,x/100,x%10
           #print "Before: ",len(dictionary[x])
           result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
           #print "After: ",len(dictionary[x])
           rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
           #print high,sc
           if sc < high:
             high = sc 
             bsoln = rsoln
             #print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
             #print bsoln.dec

      #print bsoln.dec     W
      return bsoln,high,model


class Seive7_3(Seive7):
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length of data: ",len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]
    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      #its assumed east is heaven
      return [self.gale_mutate(model,point,c,east,west) for point in easts]
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
        #its assumed east is heaven
      return [self.gale_mutate(model,point,c,west,east) for point in easts]


  def gale_mutate(self,model,point,c,east,west,multiplier = 3):
    #tooFar = multiplier * abs(c)
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
        # if x != new.dec[i] : print "blah",new.dec[i]-x
        # else: print "boom"
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      # print "Distance: ",abs(newDistance), "toofar: ",abs(tooFar)
      # print "Blown away"
      return point

  def tgenerate(self,m,pop,gen=0):
    it = int(myoptions['Seive7_2']['tgen'])
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand,-1,-1)
      #print one.dec
      pop += [one]
    return pop

  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        return False
    return True

  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(50):
      for _ in xrange(500):
        dec = []
        for constraint in constraints:
          #lo,hi = self.one(model,constraint )
          #print constraint
          lo,hi = constraint[1][0],constraint[1][1]
          temp = any(lo,hi)
          assert(temp >= lo and temp <= hi),"ranges are messed up"
          dec.append(temp)
        points.append(self.generateSlot(model,dec,-1,-1))
      #print "After Generation: ",len(points)
      points = self.fastmap(model,points)
      points += return_points(model,100)
      #print "After FastMap: ",len(points)
      points = self.tgenerate(model,points)
    print ">>>>>>>Final: ",len(points)
    #raise Exception("asdasdasffd")
    #print "\n\n",points
    #assert(len(points) == 940),"all the points were not generated"
    return points



  def evaluate(self,points=[],depth=0):
      def generate_dictionary(points=[]):  
        dictionary = {}
        chess_board = whereMain(self.model,points) #checked: working well
        for i in range(1,9):
          for j in range(1,9):
            temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
            if(len(temp)!=0):
              index=temp[0].xblock*100+temp[0].yblock
              dictionary[index] = temp
              assert(len(temp)==len(dictionary[index])),"something"
        return dictionary

      def thresholdCheck(index,dictionary):
        try:
          #print "Threshold Check: ",self.threshold
          if(len(dictionary[index])>self.threshold):return True
          else:return False
        except:
          return False
      def indexof(lsts,number,index = lambda x: x[1]):
        for i,lst in enumerate(sorted(lsts,key = index)):   
          if number == index(lst): return i
        return -1 
      def uscore(lsts,starti,endi):
        summ = 0
        for i in xrange(starti,endi+1):
          summ += lsts[i][-1]
        return summ/(endi-starti+1)

      model = self.model
      minR = model.minR
      maxR = model.maxR
      if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
        points = return_points(model,60)
        for point in points:
          point.score = score(model,point)[-1]
        
        points = [point.dec+[point.score] for point in points]
        constraints = []
        for i in xrange(len(points[0])-1):
          constraint = []
          cohen=0.3
          h = 1e6
          #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
          #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
          for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
            starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
            endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
            #print "Starti: ",starti, "Endi: ",endi
            mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
            #print "-----------------Mean Score: ",mean_score
            if mean_score < h:
              const1 = d[1][0][i]
              const2 = d[1][-1][i]
              h = mean_score
              #print "+++++++++++++++High Mean Score: ",h
          #constraint.append()

          
          constraints.append([i]+[(const1,const2)])  
        # print constraints
        # raise Exception(":asd")    
        points = self.generate2(model,constraints)
        points += self.generate2(model,constraints)
        points += return_points(model,100)



        #print "SDIV working!"
      #print "Initial Points: ",len(points)
      dictionary = generate_dictionary(points)
      # for key in dictionary.keys():
      #   if len(dictionary[key]) == 0: print ">>>>>>>>>>>>>>>>>>>>>>>"
      #   print "Key: ",key," Length: ",len(dictionary[key])
      # raise Exception("asdaskdj")

      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Depth: %d #points: %d"%(depth,len(points))
      from collections import defaultdict
      graph = defaultdict(list)
      matrix = [[0 for x in range(8)] for x in range(8)]
      for i in xrange(1,9):
        for j in xrange(1,9):
          if(thresholdCheck(i*100+j,dictionary)==False):
            result,dictionary = self.generateNew(model,i,j,dictionary)
            if result == False: 
              matrix[i-1][j-1] = 100
              #print "in middle of desert"
              continue
          matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

          
         # print matrix[i-1][j-1],
        #print
      for i in xrange(1,9):
        for j in xrange(1,9):
          #print "%0.3f"%matrix[i-1][j-1],
          sumn=0
          s = matrix[i-1][j-1]
          neigh = self.listofneighbours(i,j)
          sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
          if (i*100+j) in dictionary:
            graph[int(sumn)].append(i*100+j)
        #print
      
      #print graph[8]
      high = 1e6
      bsoln = None
      if len(graph.keys()) != 0:
	      maxi = max(graph.keys())
	      for x in graph[maxi]:
	         #print "The cell is: ",x," depth is: ",depth
	         if depth == int(myoptions['Seive3']['depth']):
	           #for i in xrange(0,5):
	             y = any(dictionary[x])
	             #print y
	             temp2 = score(model,y)[-1]
	             if temp2 < high:
	               high = temp2
	               bsoln = y
	               #print ">>>>>>>>>>>>>>>>>>>>>>>changed!"
	               #print bsoln.dec

	             #print temp2,high,bsoln.dec
	             #print
	         
	         if(depth < int(myoptions['Seive3']['depth']) and len(dictionary[x]) > 2):
	           #print "RECURSE"
	           #print "Cell No: ",x,x/100,x%10
	           #print "Before: ",len(dictionary[x])
	           #result,dictionary = self.generateNew(model,int(x/100),x%10,dictionary,True)
	           #print "After: ",len(dictionary[x])
	           rsoln,sc,model = self.evaluate(dictionary[x],depth+1)
	           #print high,sc
	           if sc < high:
	             high = sc 
	             bsoln = rsoln
	             print "Changed2!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	             #print bsoln.dec

      #print bsoln.dec     W
      return bsoln,high,model

class Seive2_Initial(Seive7):
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length of data: ",len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]
    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      #its assumed east is heaven
      return [self.gale_mutate(model,point,c,east,west) for point in easts]
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
        #its assumed east is heaven
      return [self.gale_mutate(model,point,c,west,east) for point in easts]


  def gale_mutate(self,model,point,c,east,west,multiplier = 4.5):
    #tooFar = multiplier * abs(c)
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
        # if x != new.dec[i] : print "blah",new.dec[i]-x
        # else: print "boom"
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      # print "Distance: ",abs(newDistance), "toofar: ",abs(tooFar)
      #print "Blown away"
      return point

  def tgenerate(self,m,pop,gen=0):
    it = int(myoptions['Seive2_Initial']['tgen'])
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand,-1,-1)
      #print one.dec
      pop += [one]
    return pop

  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        return False
    return True

  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(30):
      for _ in xrange(400):
        dec = []
        for constraint in constraints:
          #lo,hi = self.one(model,constraint )
          #print constraint
          lo,hi = constraint[1][0],constraint[1][1]
          temp = any(lo,hi)
          assert(temp >= lo and temp <= hi),"ranges are messed up"
          dec.append(temp)
        points.append(self.generateSlot(model,dec,-1,-1))
      #print "After Generation: ",len(points)
      points = self.fastmap(model,points)
      points += return_points(model,100)
      #print "After FastMap: ",len(points)
      points = self.tgenerate(model,points)
    #print ">>>>>>>Final: ",len(points)
    #raise Exception("asdasdasffd")
    #print "\n\n",points
    #assert(len(points) == 940),"all the points were not generated"
    return points


  def evaluate(self,points=[],depth=4):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      #print chess_board
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      #print dictionary.keys()
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def indexof(lsts,number,index = lambda x: x[1]):
      for i,lst in enumerate(sorted(lsts,key = index)):   
        if number == index(lst): return i
      return -1 
    def uscore(lsts,starti,endi):
      summ = 0
      for i in xrange(starti,endi+1):
        summ += lsts[i][-1]
      return summ/(endi-starti+1)

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

          #if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
    points = return_points(model,60)
    for point in points:
      point.score = score(model,point)[-1]
    
    points = [point.dec+[point.score] for point in points]
    constraints = []
    for i in xrange(len(points[0])-1):
      constraint = []
      cohen=0.3
      h = 1e6
      #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
      #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
      for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
        starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
        endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
        #print "Starti: ",starti, "Endi: ",endi
        mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
        #print "-----------------Mean Score: ",mean_score
        if mean_score < h:
          const1 = d[1][0][i]
          const2 = d[1][-1][i]
          h = mean_score
          #print "+++++++++++++++High Mean Score: ",h
      #constraint.append()

      
      constraints.append([i]+[(const1,const2)])  
    # print constraints
    # raise Exception(":asd")    
    points = self.generate2(model,constraints)
    #print "Number of points: ",len(points)
    print model.no_eval
    dictionary = generate_dictionary(points)
    # for key in dictionary.keys():
    #   try:
    #     print "Key: ",key, "Number: ",len(dictionary[key])
    #   except:
    #     print "Empty"


    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9): 
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            matrix[i-1][j-1] = 100
            print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    if len(graph.keys()) != 0:
	    maxi = max(graph.keys())
	    #print graph.keys()
	    #print "Number of points: ",len(graph[maxi])
	    for x in graph[maxi]:
	       #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
	       #if(len(dictionary[x]) < 15: [self.n_i(model,dictionary,x) for _ in xrange(20)]
	       #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
	       for y in dictionary[x]:
	         temp2 = score(model,y)[-1]
	         if temp2 < high:
	           high = temp2
	           bsoln = y
	    #print count     
    return bsoln.dec,high,model


class DE2(SearchersBasic):
  def __init__(self,modelName,displayS,bmin,bmax):
    self.model=modelName
    self.displayStyle=displayS
    self.model.minVal = bmin
    self.model.maxVal = bmax

  def threeOthers(self,frontier,one):
    #print "threeOthers"
    seen = [one]
    def other():
      #print "other"
      for i in xrange(len(frontier)):
        count = 10
        while True:
          if count == 0: return frontier[k]
          else: count -= 1
          k = random.randint(0,len(frontier)-1)
          if frontier[k] not in seen:
            seen.append(frontier[k])
            break
          #print "+",seen,frontier[k]
        return frontier[k]
    this = other()
    that = other()
    then = other()
    return this,that,then
  
  def trim(self,x,i)  : # trim to legal range
    m=self.model
    return max(m.minR[i], min(x, m.maxR[i]))      

  def extrapolate(self,frontier,one,f,cf):
    #print "Extrapolate"
    two,three,four = self.threeOthers(frontier,one)
    #print two,three,four
    solution=[]
    for d in xrange(self.model.n):
      x,y,z=two[d],three[d],four[d]
      if(random.random() < cf):
        solution.append(self.trim(x + f*(y-z),d))
      else:
        solution.append(one[d]) 
    return solution

  def update(self,m,f,cf,frontier,total=0.0,n=0):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
    def better(old,new):
      assert(len(old)==len(new)),"MOEAD| Length mismatch"
      for i in xrange(len(old)-1): #Since the score is return as [values of all objectives and energy at the end]
        if old[i] > new[i]: pass
        else: return False
      return True
    #print "update %d"%len(frontier)
    changed = False
    model=self.model
    newF = []
    total,n=0,0
    #print frontier 
    for x in frontier:
      #print "x: ",x,len(frontier)
      #print "eval: ",model.evaluate(x)
      s = model.evaluate(x)[:-1]
      new = self.extrapolate(frontier,x,f,cf)
      #print new
      tnew = [] 
      for i,j in enumerate(new):
        tnew.append(trim(m,j,i))


      newe=model.evaluate(tnew)[:-1]
      if better(s,newe) == True and s[-1] > newe[-1]:
        newF.append(tnew)
        changed = True
      else:
        newF.append(x)
    return newF,changed

  def sdiv(self,lst, tiny=3,cohen=0.3,
             num1=lambda x:x[0], num2=lambda x:x[1]):
      "Divide lst of (num1,num2) using variance of num2."
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
        lhs,rhs = Counts(), Counts(num2(x) for x in this)
        n0, least, cut = 1.0*rhs.n, rhs.sd(), None
        for j,x  in enumerate(this): 
          if lhs.n > tiny and rhs.n > tiny: 
            maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
            if maybe < least :  
              if abs(lhs.mu - rhs.mu) >= small: # where's the paper for this method?
                cut,least = j,maybe
          rhs - num2(x)
          lhs + num2(x)    
        return cut,least
      #----------------------------------------------
      def recurse(this, small,cuts):
        #print this,small
        cut,sd = divide(this,small)
        if cut: 
          recurse(this[:cut], small, cuts)
          recurse(this[cut:], small, cuts)
        else:   
          cuts += [(sd,this)]
        return cuts
      #---| main |-----------------------------------
      # for x in lst:
      #   print num2(x)
      small = Counts(num2(x) for x in lst).sd()*cohen # why we use a cohen??? how to choose cohen
      if lst: 
        return recurse(sorted(lst,key=num1),small,[])

  def indexof(self,lsts,number,index = lambda x: x[1]):
    for i,lst in enumerate(sorted(lsts,key = index)):
      if number == index(lst): return i
    return -1 

  def uscore(self,lsts,starti,endi):
    summ = 0
    for i in xrange(starti,endi+1):
      summ += lsts[i][-1]
    return summ/(endi-starti+1)

  def constraint_check(self,model):
    print int(myoptions['DE2']['initial'])
    points = [[model.minR[i]+random.random()*(model.maxR[i]-model.minR[i]) for i in xrange(model.n)]
               for _ in xrange(int(myoptions['DE2']['initial']))]
    scores = []
    for point in points: scores.append(model.evaluate(point)[-1])
    points = [point +[scores[i]] for i,point in enumerate(points)]
    constraints = []

    for i in xrange(len(points[0])-1):
      constraint = []
      cohen=0.3
      h = 1e6
      #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
      #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
      for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
        starti = self.indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
        endi =  self.indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
        # print "Starti: ",starti, "Endi: ",endi
        mean_score = self.uscore(sorted(points,key = lambda x:x[i]),starti,endi)
        #print "-----------------Mean Score: ",mean_score
        if mean_score < h:
          const1 = d[1][0][i]
          const2 = d[1][-1][i]
          h = mean_score
      constraints.append([i]+[(const1,const2)]) 
    for constraint in constraints:
      print constraint
    raise Exception('STOP')

    return constraints



  def evaluate(self,repeat=100,np=100,f=0.75,cf=0.3,epsilon=0.01,lives=4):
    #print "evaluate"
    model=self.model
    minR = model.minR
    maxR = model.maxR

    constraints = self.constraint_check(model)
    for i,constraint in enumerate(constraints):
      model.minR[i] = constraint[1][0]
      model.maxR[i] = constraint[1][1]

    #model.baseline(minR,maxR)
    frontier = [[model.minR[i]+random.random()*(model.maxR[i]-model.minR[i]) for i in xrange(model.n)]
               for _ in xrange(np)]
    #print frontier
    changed = False
    for i in xrange(repeat):
      if lives == 0: break
      frontier,changed = self.update(model,f,cf,frontier)

      self.model.evalBetter()
      if changed == False: 
        lives -= 1
        print "lost it"
    minR=9e10
    for x in frontier:
      #print x
      energy = self.model.evaluate(x)[-1]
      if(minR>energy):
        minR = energy
        solution=x 
    print solution,minR
    return solution,minR,self.model



class SDIV(Seive7):
  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length of data: ",len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = score(model,west)[-1]
    es = score(model,east)[-1]
    #print "West: ",ws
    #print "East: ",es
    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      #its assumed east is heaven
      return [self.gale_mutate(model,point,c,east,west) for point in easts]
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
        #its assumed east is heaven
      return [self.gale_mutate(model,point,c,west,east) for point in easts]


  def gale_mutate(self,model,point,c,east,west,multiplier = 3):
    #tooFar = multiplier * abs(c)
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
        # if x != new.dec[i] : print "blah",new.dec[i]-x
        # else: print "boom"
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    
    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      # print "Distance: ",abs(newDistance), "toofar: ",abs(tooFar)
      # print "Blown away"
      return point

  def tgenerate(self,m,pop,gen=0):
    it = int(myoptions['Seive7_2']['tgen'])
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand,-1,-1)
      #print one.dec
      pop += [one]
    return pop

  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        return False
    return True

  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(20):
      for _ in xrange(200):
        dec = []
        for constraint in constraints:
          #lo,hi = self.one(model,constraint )
          #print constraint
          lo,hi = constraint[1][0],constraint[1][1]
          temp = any(lo,hi)
          assert(temp >= lo and temp <= hi),"ranges are messed up"
          dec.append(temp)
        points.append(self.generateSlot(model,dec,-1,-1))
      #print "After Generation: ",len(points)
      points = self.fastmap(model,points)
      #print "After FastMap: ",len(points)
      points = self.tgenerate(model,points)
    #print ">>>>>>>Final: ",len(points)
    #raise Exception("asdasdasffd")
    #print "\n\n",points
    #assert(len(points) == 940),"all the points were not generated"
    return points


  def evaluate(self,points=[],depth=4):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      #print chess_board
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      #print dictionary.keys()
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False
    def indexof(lsts,number,index = lambda x: x[1]):
      for i,lst in enumerate(sorted(lsts,key = index)):   
        if number == index(lst): return i
      return -1 
    def uscore(lsts,starti,endi):
      summ = 0
      for i in xrange(starti,endi+1):
        summ += lsts[i][-1]
      return summ/(endi-starti+1)

    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

          #if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
    oracle = []
    generation = 10
    patience = 4
    bsoln = []
    high = 1e6
    points = []
    for gen in xrange(generation):

      points += return_points(model,100)  
      for point in points:
        point.score = scores(model,point)[-1]  
      temp_points = [point.dec+[point.score] for point in points]
      #oracle += temp_points
      #points = oracle
      #print "# points: ",len(temp_points)
      # oracle = sorted(points,key=lambda x:x[-1])[:100]
      # print "after fastmap: ",len(oracle)
      # points = oracle[:60]
      
      #-------------|Early Termination|--------------#
      old = high
      for point in temp_points:
        if old > point[-1]: 
          old = point[-1]
          old_soln = point[:-1]
      if old == high: patience -= 1
      else: 
        high = old
        bsoln = old_soln
      #-------------|Early Termination|--------------#
      if patience == 0: break
      #print "Minimum energy in generation ",gen," is: ",high
      constraints = []
      for i in xrange(len(temp_points[0])-1):
        constraint = []
        cohen=0.3
        h = 1e6
        for d in  self.sdiv(temp_points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
          starti = indexof([point[:-1] for point in temp_points],d[1][0][i],lambda x:x[i])
          endi =  indexof([point[:-1] for point in temp_points],d[1][-1][i],lambda x:x[i])
          #print "Starti: ",starti, "Endi: ",endi
          mean_score = uscore(sorted(temp_points,key = lambda x:x[i]),starti,endi)
          if mean_score < h:
            const1 = d[1][0][i]
            const2 = d[1][-1][i]
            h = mean_score
        constraints.append([i]+[(const1,const2)]) 
      for constraint in constraints:
        model.minR[int(constraint[0])] = constraint[1][0]
        model.maxR[int(constraint[0])] = constraint[1][1]
        # print "Index: ",int(constraint[0]),
        # print "Low: ",constraint[1][0],
        # print "High: ",constraint[1][1]

    # print constraints
    # raise Exception(":asd")    
    # points = self.generate2(model,constraints)
    # #print "Number of points: ",len(points)

    # dictionary = generate_dictionary(points)
    # for key in dictionary.keys():
    #   try:
    #     print "Key: ",key, "Number: ",len(dictionary[key])
    #   except:
    #     print "Empty"


    # from collections import defaultdict
    # graph = defaultdict(list)
    # matrix = [[0 for x in range(8)] for x in range(8)]
    # for i in xrange(1,9):
    #   for j in xrange(1,9): 
    #     # try:
    #     # 	print i,j,len(dictionary[i*100+j])
    #     # except:
    #     # 	print "empty"

    #     if(thresholdCheck(i*100+j,dictionary)==False):
    #       #result,dictionary = self.generateNew(self.model,i,j,dictionary)
    #       #if result == False: 
    #         matrix[i-1][j-1] = 100
    #         print "in middle of desert"
    #         continue
    #     matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]
   

        
    #    # print matrix[i-1][j-1],
    #   #print
    # for i in xrange(1,9):
    #   for j in xrange(1,9):
    #     sumn=0
    #     s = matrix[i-1][j-1]
    #     neigh = self.listofneighbours(i,j)
    #     sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
    #     if (i*100+j) in dictionary:
    #       graph[int(sumn)].append(i*100+j)
        
    # high = 1e6
    # bsoln = None
    # maxi = max(graph.keys())
    # #print graph.keys()
    # # print "Number of points: ",len(graph[maxi])
    # # print "Points: ",graph[maxi]
    
    # count = 0
    # for x in graph[maxi]:
    #    #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
    #    #if(len(dictionary[x]) < 15: [self.n_i(model,dictionary,x) for _ in xrange(20)]
    #    #print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
    #    for y in dictionary[x]:
    #      temp2 = score(model,y)[-1]
    #      count += 1
    #      if temp2 < high:
    #        print x
    #        high = temp2
    #        bsoln = y
    # #print count   
    # raise Exception("STOP")  
    return bsoln,high,model


class Seive2I_ExtraSDIV(Seive7):
  all_points = []



  """
  Find the furthest pair in all pairs!NO RANDOM!! Mr. Fu's code
  """
  def allfurthest(self,m, data):
    # temp = -10**10 # if it was 0, will casue "NoneType pair" error
    temp = -10**10
    furthestpair = None
    for i in data:
      for j in data:
        c = dist(m, i,j)
        if c > temp:
          temp = c
          furthestpair =[i,j,c]
    return furthestpair

  def fastmap(self,model,data):
    "Divide data into two using distance to two distant items."
    #print ">>>>>>>>>>>>>>>>>>.FastMap"
    #print "Length of data: ",len(data)
    one  = any(data)             # 1) pick anything
    west = furthest(model,one,data)  # 2) west is as far as you can go from anything
    east = furthest(model,west,data) # 3) east is as far as you can go from west
    c    = dist(model,west,east)

    # pair = self.allfurthest(model,data)
    # west = pair[0]
    # east = pair[1]
    # c = pair[2]
    # now find everyone's distance
    xsum, lst = 0.0,[]
    ws = scores(model,west)[-1]
    es = scores(model,east)[-1]
    #--------------|add to repo|--------------#
    self.all_points.append(west)
    self.all_points.append(east)
    #print "All points2 : ",len(self.all_points)

    if ws > es: print es
    else: print ws

    for one in data:
      a = dist(model,one,west)
      b = dist(model,one,east)
      x = (a*a + c*c - b*b)/(2*c) # cosine rule
      xsum += x
      lst  += [(x,one)]
    # now cut data according to the mean distance
    if ws > es:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
      #its assumed east is heaven
      return [self.gale_mutate(model,point,c,east,west) for point in easts]
    else:
      cut, wests, easts = xsum/len(data), [], []
      for x,one in lst:
        where = wests if x < cut else easts 
        where += [one]
        #its assumed east is heaven
      return [self.gale_mutate(model,point,c,west,east) for point in easts]


  def gale_mutate(self,model,point,c,east,west,multiplier = 1.5):
    #tooFar = multiplier * abs(c)
    #print "C: ",c
    tooFar = multiplier * abs(c)
    import copy
    new = copy.deepcopy(point)
    for i in xrange(len(point.dec)):
      d = east.dec[i] - west.dec[i]
      if not d == 0:
        d = -1 if d < 0 else 1
        #d = east.dec[i] = west.dec[i]
        x = new.dec[i] * (1 + abs(c) * d)
        new.dec[i] = max(min(hi(model,i),x),lo(model,i))
        # if x != new.dec[i] : print "blah",new.dec[i]-x
        # else: print "boom"
    newDistance = self.project(model,west,east,c,new) -\
                  self.project(model,west,east,c,west)
    
    if abs(newDistance) > tooFar: print "push worked"

    if abs(newDistance) < tooFar  and self.valid(model,new):
      return new
    else:
      # print "Distance: ",abs(newDistance), "toofar: ",abs(tooFar)
      #print "Blown away"
      return point

  def tgenerate(self,m,pop,gen=0):
    it = int(myoptions['Seive2_Initial']['tgen'])
    for _ in xrange(it):
      temp = random.random()
      o = any(pop)
      t = any(pop)
      th = any(pop)
      if temp <= 0.5:  cand = polate(m,o.dec,t.dec,th.dec,0.1,0.5)
      else: cand = polate(m,o.dec,t.dec,th.dec,0.9,2.0)
      one = self.generateSlot(m,cand,-1,-1)
      #print one.dec
      pop += [one]
    return pop

  def polate(m,lx,ly,lz,fmin,fmax):
    def lo(m,index)      : return m.minR[index]
    def hi(m,index)      : return m.maxR[index]
    def trim(m,x,i)  : # trim to legal range
      temp = min(hi(m,i),max(lo(m,i),x))
      assert( lo(m,i) <= temp and hi(m,i) >= temp),"error"
      return temp
    def indexConvert(index):
      return int(index/100),index%10

    assert(len(lx)==len(ly)==len(lz))
    cr=0.3
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr:
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(m,x + probEx*(y-z),i)
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint
  def project(self,model,west, east, c, x):
    "Project x onto line east to west"
    if c == 0: return 0
    a = dist(model,x,west)
    b = dist(model,x,east)
    return (a*a + c*c - b*b)/(2*c) # cosine rule

  def valid(self,m,val):
    for x in xrange(len(val.dec)):
      if not m.minR[x] <= val.dec[x] <= m.maxR[x]: 
        return False
    return True

  def generate2(self,model,constraints):
    def any(l,h):
      #print ">>>>>>>> : ",lo,hi  
      return (l + random.random()*(h-l))
    points = []
    for _ in xrange(100):
      for _ in xrange(400):
        dec = []
        for constraint in constraints:
          #lo,hi = self.one(model,constraint )
          #print constraint
          lo,hi = constraint[1][0],constraint[1][1]
          temp = any(lo,hi)
          assert(temp >= lo and temp <= hi),"ranges are messed up"
          dec.append(temp)
        points.append(self.generateSlot(model,dec,-1,-1))

      points = self.fastmap(model,points)
      points += return_points(model,100)
      points = self.tgenerate(model,points)
      if len(self.all_points) % 20 == 0:
        print "constraints changed"
        constraints = self.sdiv_mod(self.all_points)
        #print "New: ",constraints
      counter = 0
    return points


  def sdiv_mod(self,points2):
    def indexof(lsts,number,index = lambda x: x[1]):
      for i,lst in enumerate(sorted(lsts,key = index)):   
        if number == index(lst): return i
      return -1 
    def uscore(lsts,starti,endi):
      summ = 0
      for i in xrange(starti,endi+1):
        summ += lsts[i][-1]
      return summ/(endi-starti+1)
 
    points = [point.dec+[point.scores[-1]] for point in points2]
    constraints = []
    for i in xrange(len(points[0])-1):
      constraint = []
      cohen=0.3
      h = 1e6
      #print self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1])[0][1][i]
      #print "........................>>",len(self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]))
      for d in  self.sdiv(points,cohen=cohen,num1=lambda x:x[i],num2=lambda x:x[-1]):
        starti = indexof([point[:-1] for point in points],d[1][0][i],lambda x:x[i])
        endi =  indexof([point[:-1] for point in points],d[1][-1][i],lambda x:x[i])
        #print "Starti: ",starti, "Endi: ",endi
        mean_score = uscore(sorted(points,key = lambda x:x[i]),starti,endi)
        #print "-----------------Mean Score: ",mean_score
        if mean_score < h:
          const1 = d[1][0][i]
          const2 = d[1][-1][i]
          h = mean_score
      constraints.append([i]+[(const1,const2)]) 
    return constraints

  def evaluate(self,points=[],depth=4):
    def generate_dictionary(points=[]):  
      dictionary = {}
      chess_board = whereMain(self.model,points) #checked: working well
      #print chess_board
      for i in range(1,9):
        for j in range(1,9):
          temp = [x for x in chess_board if x.xblock==i and x.yblock==j]
          if(len(temp)!=0):
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"
      #print dictionary.keys()
      return dictionary

    def thresholdCheck(index,dictionary):
      try:
        #print "Threshold Check: ",index
        if(len(dictionary[index])>self.threshold):return True
        else:return False
      except:
        return False


    model = self.model
    minR = model.minR
    maxR = model.maxR
    #if depth == 0: model.baseline(minR,maxR)

          #if depth == 0 and len(points) == 0: 
        #generate points according to the constraints
    points = return_points(model,60)
    for point in points: scores(model,point)[-1]



    #-------------| add to repo|------------------------#
    self.all_points.extend(points)
    print "All points : ",len(self.all_points)
    
    constraints = self.sdiv_mod(points)
 
    # print constraints
    # raise Exception(":asd")    
    points = self.generate2(model,constraints)
    #print "Number of points: ",len(points)
    print "Points Evaluated: ",len(self.all_points)
    dictionary = generate_dictionary(points)
    # for key in dictionary.keys():
    #   try:
    #     print "Key: ",key, "Number: ",len(dictionary[key])
    #   except:
    #     print "Empty"


    from collections import defaultdict
    graph = defaultdict(list)
    matrix = [[0 for x in range(8)] for x in range(8)]
    for i in xrange(1,9):
      for j in xrange(1,9): 
        if(thresholdCheck(i*100+j,dictionary)==False):
          result,dictionary = self.generateNew(self.model,i,j,dictionary)
          if result == False: 
            matrix[i-1][j-1] = 100
            print "in middle of desert"
            continue
        matrix[i-1][j-1] = score(model,self.one(model,dictionary[i*100+j]))[-1]

        
       # print matrix[i-1][j-1],
      #print
    for i in xrange(1,9):
      for j in xrange(1,9):
        sumn=0
        s = matrix[i-1][j-1]
        neigh = self.listofneighbours(i,j)
        sumn = sum([1 for x in neigh if matrix[self.rowno(x)-1][self.colmno(x)-1]>s])
        if (i*100+j) in dictionary:
          graph[int(sumn)].append(i*100+j)
        
    high = 1e6
    bsoln = None
    if len(graph.keys()) != 0:
      maxi = max(graph.keys())
      #print graph.keys()
      #print "Number of points: ",len(graph[maxi])
      for x in graph[maxi]:
         #print "Seive2:B Number of points in ",maxi," is: ",len(dictionary[x])
         #if(len(dictionary[x]) < 15: [self.n_i(model,dictionary,x) for _ in xrange(20)]
         print "Seive2:A Number of points in ",maxi," is: ",len(dictionary[x])
         for y in dictionary[x]:
           temp2 = scores(model,y)[-1]
           if temp2 < high:
             high = temp2
             bsoln = y
      #print count     
    return bsoln.dec,high,model