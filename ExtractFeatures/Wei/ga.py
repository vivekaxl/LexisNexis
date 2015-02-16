from __future__ import division
from log import *
from models import *
from xtile import *
from base import *
import sys,random, math, datetime, time,re, pdb, operator
sys.dont_write_bytecode = True

# @printlook 
def ga(model):
  mutationRate = 1/model.n 
  population = []
  solution =[]
  children = []
  fitness = {}
  history = {}
  mateNum = 20
  def selection(sortedFitness):
    return [population[sortedFitness[0][0]], population[sortedFitness[1][0]]] # sroted[0] and [1] are the smallest two we preferred
  def crossover(selected):
    '''crossover will do this way: offsprint1 = p* parent 1+ (1-p)* parent2 for numbers between two points '''
    def what(lst):
      return lst[0] if isinstance(lst, list) else lst
    children1 = []
    if rand()> Settings.ga.crossRate:
      return selected[0]
    else:
      if model.n ==1:
        children1 = [(what(selected[0]) + what(selected[1]))*0.5]
      else:
        index = sorted([random.randint(0, model.n - 1) for _ in xrange(Settings.ga.crossPoints)])
        parent1 = selected[0]
        parent2 = selected[1]
        children1 = parent1[:]
        children1[index[0]:index[1]] = parent2[index[0]:index[1]]
      return children1
  def mutate(children, selected):
    # print children
    for k, n in enumerate(children):
      if rand()< mutationRate:
        children[k]= selected[random.randint(0,1)][random.randint(0, model.n-1)] # pick value from mom or dad
    # print children
    return children
  def tournament(sortedFitness, m=10): # do tornament selection, select the best daddy or mom in  m = 10 candidates
    index = []
    for _ in range(m):
      index.append(random.randint(0, Settings.ga.pop-1))
    betterIndex = list(set(sorted(index)))
    parentlst = [population[sortedFitness[betterIndex[0]][0]], population[sortedFitness[betterIndex[1]][0]]]
    return parentlst
  def fit(fitness):
    sortedFitness = sorted(fitness.items(), key = lambda x:x[1]) # a sorted list    
    return sortedFitness[:Settings.ga.pop] # just return the top 50 candidates as new populatioin
  def produce(selected):
  	children = crossover(selected)
  	children = mutate(children, selected)
  	return children

  min_energy, max_energy = model.baseline()
  eb= 0
  solution = []
  control = Control(model, history)
  for _ in xrange(Settings.ga.pop):
    temp = model.generate_x()
    population.append(temp)
  # for num in Settings.ga.genNum:
  t = 0
  while(t < Settings.ga.genNum): # figure stop out
    stopsign = control.next(t) #true ---stop
    if stopsign:
      break
    for (k, xlst) in enumerate(population):
      fitness[k] = model.getDepen(xlst) 
    newpopfitness = fit(fitness)
    for n, k in newpopfitness:
      population[n] = population[newpopfitness[0][0]] # new generation
      control.logxy(population[n])
    # for n, k in population:
    #   control.logxy(k) # log new generation
    eb = model.norm(newpopfitness[0][1])
    solution = population[newpopfitness[0][0]]
    for _ in range(mateNum):
      selected = tournament(newpopfitness)
      children.append(produce(selected))
    population.extend(children)
    t +=1
  # print "best solution : %s" % str(solution)
  # print "best normalized results: %s" % str(eb)  
  # print "-"*20
  # printReport(model)
  # lohi=printRange(model)
  # return eb,lohi
  if Settings.other.xtile: 
    printReport(model, history)
    print "\n"
    printSumReport(model, history)
  if Settings.other.reportrange:
    rrange=printRange(model, history)
    return eb,rrange
  else:
    return eb

def startga():
  for klass in [Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
  # for klass in [DTLZ7]:
    print "="*50
    print "!!!!", klass.__name__, 
    print "\nSearcher: GA"
    reseed()
    ga(klass())


if __name__ == "__main__":startga()
     # print sortedFitness




    

