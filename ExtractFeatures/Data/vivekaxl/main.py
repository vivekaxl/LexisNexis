from __future__ import division 
import sys 
import random
import math 
import numpy as np
from where_mod import *
sys.dont_write_bytecode = True
rand=random.random
# consist of dictionary where the index is 
# 100*xblock+yblock and 
 
threshold =10         #threshold for number of points to be considered as a prospective solution
ncol=8               #number of columns in the chess board
nrow=8               #number of rows in the chess board
intermaxlimit=20     #Max number of points that can be created by interpolation
extermaxlimit=20     #Max number of points that can be created by extrapolation
evalscores=0

#There is something wrong with the lambda expressions need to make sure it wraps around.
convert = lambda x,y: (x*100)+y
rowno = lambda x: int(x/100)
colmno = lambda x: x%10

def gonw(x):
  if(rowno(x)==1 and colmno(x)==1):return convert(nrow,ncol)#in the first coulumn and first row
  elif(rowno(x)==1): return convert(nrow,colmno(x)-1)
  elif(colmno(x)==1): return convert(rowno(x)-1,ncol)#in the first column
  else: return (x-101)

def gow(x):
 if(colmno(x)==1): return convert(rowno(x),ncol)
 else: return (x-1)

def gosw(x):
  if(rowno(x)==nrow and colmno(x)==1): return convert(1,ncol)
  elif(rowno(x)==nrow): return convert(1,colmno(x)-1)
  elif(colmno(x)==1): return convert(rowno(x)+1,ncol)
  else: return (x+99)

def gos(x):
  if(rowno(x)==nrow): return convert(1,colmno(x))
  else: return x+100

def gose(x):
  if(rowno(x)==nrow and colmno(x)==ncol): return convert(1,1)
  elif(rowno(x)==nrow): return convert(1,colmno(x)+1)
  elif(colmno(x)==ncol): return convert(rowno(x)+1,1)
  else: return x+101

def goe(x):
  if(colmno(x)==ncol): return convert(rowno(x),1)
  else: return x+1

def gone(x):
  if(rowno(x)==1 and colmno(x)==ncol): return convert(nrow,1)
  elif(rowno(x)==1): return convert(nrow,colmno(x)+1)
  elif(colmno(x)==ncol): return convert(rowno(x)-1,1)
  else: return x-99

def gon(x):
  if(rowno(x)==1): return convert(nrow,colmno(x))
  else: return x-100 

import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

def neighbourhood(xblock,yblock):
  temp=[[-1,0,1],[-1,0,1]]
  comb=[]
  import itertools
  for e in itertools.product(*temp):
   comb.append(e)
  neigbour ={}
  def neighr(xblock,yblock):
    index=xblock*100+yblock
    try:
      #only return the neighbours who has threshold number of
      #elements in it.
      if len(dictionary[index]) > threshold:
        neigbour[index]=len(dictionary[index])
      #else:print len(dictionary[index])
    except: pass  
  for i in comb:
    neighr((xblock-i[0])%8,(yblock-i[1])%8)
  return neigbour

def stats(listl):
  def median(lst,ordered=False):
    if not ordered: lst= sorted(lst)
    n = len(lst)
    p = n//2
    if n % 2: return lst[p]
    q = p - 1
    q = max(0,min(q,n))
    return (lst[p] + lst[q])/2
  from scipy.stats import scoreatpercentile
  q1 = scoreatpercentile(listl,25)
  q3 = scoreatpercentile(listl,75)  
  #print "IQR : %f"%(q3-q1)
  #print "Median: %f"%median(listl)
  return median(listl),(q3-q1)

def energy(m,xblock,yblock,dictionary):
  global evalscores
  tempIndex=int(100*xblock+yblock)
  #print "energy| xblock: %d yblock: %d"%(xblock,yblock)
  #print "energy| TempIndex: " ,tempIndex
  energy=[]
  try:
    for x in dictionary[tempIndex]:
      if x.obj == [None]*len(objectives(m)):  evalscores+=1
        
      #print "before energy|x.changed: ",x.obj
      score(m,x)
      #print "after energy|x.changed: ",x
      #print "ENERGY| score:",x.obj
      energy.append(np.sum(x.obj))      
    median,iqr=stats(energy)
    #print "%d, %f, %f"%(len(dictionary[tempIndex]),median,iqr),
    return median,iqr
  except: return 0,0
    #print "Energy Error"
    #import traceback
    #traceback.print_exc()


def getpoints(index,dictionary):
  tempL = []
  for x in dictionary[index]:tempL.append(x.dec)
  return tempL
    
def one(m,lst): 
  def any(l,h):
    return (0 + random.random()*(h-l))
  return lst[int(any(0,len(lst) - 1)) ]  

def wrapperInterpolate(m,xindex,yindex,maxlimit,dictionary):
  def interpolate(lx,ly,cr=1,fmin=0,fmax=1):
    def lo(m)      : return 0.0
    def hi(m)      : return  1.0
    def trim(x)  : # trim to legal range
      return max(lo(x), x%hi(x))
    assert(len(lx)==len(ly))
    genPoint=[]
    for i in xrange(len(lx)):
      x,y=lx[i],ly[i]
      #print x
      #print y
      rand = random.random
      if rand < cr:
        probEx = fmin +(fmax-fmin)*rand()
        new = trim(min(x,y)+probEx*abs(x-y))
      else:
        new = y
      genPoint.append(new)
    return genPoint

  decision=[]
  #print "Number of points in ",xindex," is: ",len(dictionary[xindex])
  #print "Number of points in ",yindex," is: ",len(dictionary[yindex])
  xpoints=getpoints(xindex,dictionary)
  ypoints=getpoints(yindex,dictionary)
  import itertools 
  listpoints=list(itertools.product(xpoints,ypoints))
  #print "Length of Listpoints: ",len(listpoints)
  count=0
  while True:
    if(count>min(len(xpoints),maxlimit)):break
    x=one(m,listpoints)
    decision.append(interpolate(x[0],x[1]))
    count+=1
  return decision


def generateSlot(m,decision,x,y):
  newpoint = Slots(changed = True,
            scores=None, 
            xblock=x, #sam
            yblock=y,  #sam
            x=-1,
            y=-1,
            obj = [None] * len(objectives(m)), #[None]*4
            dec = decision)

  #scores(m,newpoint)
  #print "Decision: ",newpoint.dec
  #print "Objectives: ",newpoint.obj
  return newpoint


#There are three points and I am trying to extrapolate. Need to pass two cell numbers
def wrapperextrapolate(m,xindex,yindex,maxlimit):
  def extrapolate(lx,ly,lz,cr=1,fmin=0.9,fmax=2):
    def lo(m)      : return 0.0
    def hi(m)      : return  1.0
    def trim(x)  : # trim to legal range
      return max(lo(x), x%hi(x))
    def indexConvert(index):
      return int(index/100),index%10
    assert(len(lx)==len(ly)==len(lz))
    genPoint=[]
    for i in xrange(len(lx)):
      x,y,z = lx[i],ly[i],lz[i]
      rand = random.random()

      if rand < cr: 
        probEx = fmin + (fmax-fmin)*random.random()
        new = trim(x + probEx*(y-z))
      else:
        new = y #Just assign a value for that decision
      genPoint.append(new)
    return genPoint

  decision=[]
  #TODO: need to put an assert saying checking whether extrapolation is actually possible
  xpoints=getpoints(xindex)
  ypoints=getpoints(yindex)
  count=0
  while True:
    if(count>min(len(xpoints),maxlimit)):break
    two = one(m,xpoints)
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



"""
def decisions:
if there are enough points then look at the neighbour. Look for the cell which has 
  i.   highest number of points
  ii.  lowest mean energy. energy is a the sum of all the objectives
  iii. lowest variance
else
  if the opposite cells have threshold number of cells interpolate
  else if there are consequtive points which have threshold points then extrapolate
"""

def generateNew(m,xblock,yblock,dictionary):


  def indexConvert(index):
    return int(index/100),index%10

  def opposite(a,b):
    ax,ay,bx,by=a/100,a%100,b/100,b%100
    if(abs(ax-bx)==2 or abs(ay-by)==2):return True
    else: return False

  def thresholdCheck(index):
    try:
      #print "Threshold Check: ",index
      if(len(dictionary[index])>threshold):return True
      else:return False
    except:
      #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>except: ",index
      return False

  def interpolateCheck(xblock,yblock):
    returnList=[]
    if(thresholdCheck(gonw(convert(xblock,yblock))) and thresholdCheck(gose(convert(xblock,yblock))) == True):
      returnList.append(gonw(convert(xblock,yblock)))
      returnList.append(gose(convert(xblock,yblock)))
    if(thresholdCheck(gow(convert(xblock,yblock))) and thresholdCheck(goe(convert(xblock,yblock))) == True):
     returnList.append(gow(convert(xblock,yblock)))
     returnList.append(goe(convert(xblock,yblock)))
    if(thresholdCheck(gosw(convert(xblock,yblock))) and thresholdCheck(gone(convert(xblock,yblock))) == True):
     returnList.append(gosw(convert(xblock,yblock)))
     returnList.append(gone(convert(xblock,yblock)))
    if(thresholdCheck(gon(convert(xblock,yblock))) and thresholdCheck(gos(convert(xblock,yblock))) == True):
     returnList.append(gon(convert(xblock,yblock)))
     returnList.append(gos(convert(xblock,yblock)))
    return returnList


  def extrapolateCheck(xblock,yblock):
    #TODO: If there are more than one consequetive blocks with threshold number of points how do we handle it?
    #TODO: Need to make this logic more succint
    returnList=[]
    #go North West
    temp = gonw(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gonw(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gonw(temp))

    #go North 
    temp = gon(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gon(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gon(temp))

    #go North East
    temp = gone(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gone(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gone(temp))

    #go East
    temp = goe(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(goe(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(goe(temp))

    #go South East
    temp = gose(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gose(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gose(temp))

    #go South
    temp = gos(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gos(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gos(temp))

    #go South West
    temp = gosw(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gosw(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gosw(temp))

    #go West
    temp = gow(convert(xblock,yblock))
    result1 = thresholdCheck(temp)
    if result1 == True:
      result2 = thresholdCheck(gow(temp))
      if(result1 and result2 == True):
        returnList.append(temp)
        returnList.append(gow(temp))
    return returnList
  
  newpoints=[]
  #print "generateNew| xblock: %d yblock: %d"%(xblock,yblock)
  #print "generateNew| convert: ",convert(xblock,yblock)
  #print "generateNew|thresholdCheck(convert(xblock,yblock): ",thresholdCheck(convert(xblock,yblock))
  if(thresholdCheck(convert(xblock,yblock))==False):
    #print "generateNew| Cell is relatively sparse: Might need to generate new points"
    listInter=interpolateCheck(xblock,yblock)
    #print "generateNew|listInter: ",listInter
    if(len(listInter)!=0):
      decisions=[]
      assert(len(listInter)%2==0),"listInter%2 not 0"
      #print thresholdCheck(xb),thresholdCheck(yb)
      for i in xrange(int(len(listInter)/2)):
        decisions.extend(wrapperInterpolate(m,listInter[i*2],listInter[(i*2)+1],int(intermaxlimit/len(listInter))+1,dictionary))
        #print "generateNew| Decisions Length: ",len(decisions)
      #print "generateNew| Decisions: ",decisions
      if convert(xblock,yblock) in dictionary: pass
      else:
        #print convert(xblock,yblock)
        assert(convert(xblock,yblock)>=101),"Something's wrong!" 
        assert(convert(xblock,yblock)<=808),"Something's wrong!" 
        dictionary[convert(xblock,yblock)]=[]
      old = _checkDictionary(dictionary)
      for decision in decisions:dictionary[convert(xblock,yblock)].append(generateSlot(m,decision,xblock,yblock))
      #print "generateNew| Interpolation works!"
      new = _checkDictionary(dictionary)
      #print "generateNew|Interpolation| Number of new points generated: ", (new-old)
      return True
    else:
      #print "generateNew| Interpolation failed!"
      listExter = extrapolateCheck(xblock,yblock)
      if(len(listExter)==0):
        print "generateNew|Interpolation and Extrapolation failed|In a tight spot..somewhere in the desert RANDOM JUMP REQUIRED"
        return False
      else:
        assert(len(listExter)%2==0),"listExter%2 not 0"
        for i in xrange(int(len(listExter)/2)):
          decisions.extend(wrapperextrapolate(m,listExter[2*i],listExter[2*i]+1,int(extermaxlimit)/len(listExter)))
        if convert(xblock,yblock) in dictionary: pass
        else: 
          assert(convert(xblock,yblock)>=101),"Something's wrong!" 
          assert(convert(xblock,yblock)<=808),"Something's wrong!" 
          dictionary[convert(xblock,yblock)]=[]
        old = _checkDictionary()
        for decision in decisions: dictionary[convert(xblock,yblock)].append(generateSlot(m,decision,xblock,yblock))
        new = _checkDictionary()
        #print "generateNew|Extrapolation Worked ",len(dictionary[convert(xblock,yblock)])
        #print "generateNew|Extrapolation| Number of new points generated: ", (new-old)
        return True
  else:
    listExter = extrapolateCheck(xblock,yblock)
    if(len(listExter) == 0):
      print "generateNew| Lot of points but middle of a desert"
      return False #A lot of points but right in the middle of a deseart
    else:
      return True
  """
  print interpolateCheck(xblock,yblock)
  """

"""
Return a list of neighbours:
"""
def listofneighbours(m,xblock,yblock):
  index=convert(xblock,yblock)
  #print "listofneighbours| Index passed: ",index
  listL=[]
  listL.append(goe(index))
  listL.append(gose(index))
  listL.append(gos(index))
  listL.append(gosw(index))
  listL.append(gow(index))
  listL.append(gonw(index))
  listL.append(gon(index))
  listL.append(gone(index))
  return listL

def printNormal(m,dictionary):

  def thresholdCheck(index):
    try:
      if(len(dictionary[index])>threshold):return len(dictionary[index])
      else:return False
    except:
      return False

  for i in xrange(1,9):
    for j in xrange(1,9):
      #print '[%s]' % ', '.join(map(str, mylist))
      print "%d|%d  |"%((convert(i,j)),thresholdCheck(convert(i,j))),
      temp = energy(m,i,j,dictionary)
      print "%2.3f,%2.3f"%(temp[0],temp[1]),
      print "    ",
    print
"""
Generate random cell number pass it to generateNew() and if the point is in between a deseart then jump to a random cell
look at the neighbourhood and see which is the most promising cell to move to

"""
def searcher(m,dictionary):
  def randomC(): 
    return int(1+random.random()*7)
  def randomcell(): 
    return [randomC() for _ in xrange(2)]

  tries=0
  bmean,biqr=1e6,1e6
  bsoln=[-1,-1]
  while(tries<20):
    print "---------------------------Tries: %d---------------------------------------"%tries
    soln = randomcell()
    tries+=1
    repeat=0
    while(repeat<6):
      print "Solution being tried: %d %d "%(soln[0],soln[1])
      result = generateNew(m,soln[0],soln[1],dictionary)
      if(result == False): 
        print "In middle of the deseart"
        break
      else:
        #print "Searcher| Solution being tried: %d %d "%(soln[0],soln[1])
        smean,siqr = energy(m,soln[0],soln[1],dictionary)
        neighbours = listofneighbours(m,soln[0],soln[1])
        #print neighbours
        nmean,niqr=1e6,1e6
        for neighbour in neighbours:
          #print "Searcher| neighbour: ",neighbour
          result = generateNew(m,int(neighbour/100),neighbour%10,dictionary)
          if(result == True):
            tmean,tiqr = energy(m,int(neighbour/100),neighbour%10,dictionary)
            if(tmean<nmean or (tmean==nmean and tiqr < niqr)):
              #print "Searcher| tmean: %f mean: %f"%(tmean,mean)
              #print "Searcher| tiqr: %f iqr: %f"%(tiqr,iqr)
              nsoln = [int(neighbour/100),neighbour%10]
              #print "Searcher|btsoln: ",btsoln
              nmean=tmean
              niqr=tiqr
          else:
            #print "Searcher|NAAAAAAAAAAAAH"
            pass
        if(nmean<smean or (nmean == smean and nmean<smean)):
          soln=nsoln
          repeat+=1
        else:
          break

        if(min(nmean,smean)<bmean or (min(nmean,smean) == bmean and min(niqr,siqr)<biqr)):
          bmean=min(nmean,smean)
          biqr=min(niqr,siqr)
          if(nmean<smean or (nmean == smean and niqr<siqr)):
            bsoln=nsoln
          else: bsoln=soln

#I need to look at slope now. The number of evaluation is not reducing a lot
#need to put a visited sign somewhere to stop evaluations 


  print ">>>>>>>>>>>>>>WOW Mean:%f IQR: %f"%(bmean,biqr)
  print ">>>>>>>>>>>>>>WOW Soultion: ",bsoln


def _checkdirection(x):
  print "North: ",gon(x)
  print "North West: ",gonw(x)
  print "North East: ",gone(x)
  print "East: ",goe(x)
  print "South East: ",gose(x)
  print "South: ",gos(x)
  print "South West: ",gosw(x)
  print "West: ",gow(x)
  print "-------------------------------"

def _wrappercheckdirection():
  _checkdirection(101)
  _checkdirection(801)
  _checkdirection(808)
  _checkdirection(108)


def _checkDictionary(dictionary):
  sum=0
  for i in dictionary.keys():
    sum+=len(dictionary[i])
  return sum

def main():
  global evalscores
  dictionary ={}
  m='model'
  random.seed(32)
  chessBoard = whereMain() 
  #print x,y
  for i in range(1,9):
      for j in range(1,9):
          temp=[]
          for x in chessBoard:
              if x.xblock==i and x.yblock==j:
                  temp.append(x)
          if(len(temp)!=0):
            #print "tempList",
            #print temp[0].xblock,temp[0].yblock,len(temp)
            index=temp[0].xblock*100+temp[0].yblock
            dictionary[index] = temp
            assert(len(temp)==len(dictionary[index])),"something"

  searcher(m,dictionary)
  print "Total number of points in the grid: ",_checkDictionary(dictionary)
  print "Total number of evaluation in the grid: ",evalscores
  printNormal(m,dictionary)


if __name__ == '__main__':
  #_wrappercheckdirection()
 # _interpolate()
  main()
  #_extrapolate()
  #_neighbourhood()
