from helperFunctions import *

def findSmallestMultiple(startValue,endValue):
    if startValue==1: startValue+=1
    numList = range(startValue,endValue+1)
    primeList = SOE(endValue)
    for i in primeList:
        numList.remove(i)
    num = product = reduce(lambda x,y:x*y, primeList)
    while True:
        flag=1
        for i in numList:
            if num%i:
                flag=0
                break
        if flag==0:
            num+=product    
        else:
            return num
            
print findSmallestMultiple(1,20)

