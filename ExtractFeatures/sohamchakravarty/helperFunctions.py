from math import sqrt

#Sieve of Eratosthanes - returns a list of primes in range [0,n]
#Efficiency :O( N log logN )
def SOE(n):
    np1 = n + 1
    s = list(range(np1))
    s[1] = 0
    sqrtn = int(round(n**0.5))
    for i in xrange(2, sqrtn + 1):   
        if s[i]:
            s[i*i: np1: i] = [0] * len(xrange(i*i, np1, i)) 
    return filter(None, s)

#Function to check if a number is prime
def isPrime(n):
     return all(n%i for i in xrange(2,int(sqrt(n))+1))

#Factors of a number
#http://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n/i] for i in range(1, int(sqrt(n)) + 1) if n % i == 0)))

#Factorial of a number
def factorial(n):
    return reduce(lambda x,y:x*y,range(1,n+1))

#Function to convert list of integers into an array
def convertListToInt(arr):
    return int(''.join(map(str,arr)))

