from decimal import *
from math import sqrt

getcontext().prec = 5000

#Function to find prime numbers
def SOE(startValue,endValue):
    primes = list(range(startValue,endValue+1))
    for i in xrange(2, int(sqrt(endValue))+1):   
        primes = filter(lambda x: x==i or x%i,primes)  
    return primes

def LongestRecurringCycle(limit):
    numerator = Decimal(1)
    longestLength = 0
    value = 0
    for i in SOE(1,limit):
        decimalPart = str(numerator / i).replace('0.','')
        if all(x==decimalPart[0] for x in decimalPart):continue    #to prevent numbers with decimal part have single recurring digit
        for j in xrange(3,5000):        #the outer limit is the precision
            if decimalPart[:j]!=decimalPart[j:j+j]:
                j+=1
            else:
                if j>longestLength:
                    longestLength = j
                    value = i
                break
    print value,longestLength


LongestRecurringCycle(1000)
