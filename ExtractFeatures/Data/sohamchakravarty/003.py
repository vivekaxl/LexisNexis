from math import sqrt
from helperFunctions import *

def LargestPrimeFactor(N):
    fctrs = sorted(factors(N))
    for fctr in fctrs[::-1]:
        if isPrime(fctr):
            return fctr
    
if __name__=="__main__":
    print(LargestPrimeFactor(600851475143))
