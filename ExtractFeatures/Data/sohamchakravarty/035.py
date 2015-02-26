#My Solution

#1) Use sieve to generate prime numbers till N
#2) Start the algo for prime values>10
#3) Do not loop over values already checked
#4) Check if the prime number contains even digit before circular prime check
#5) use sets inorder to check whether list of circular primes are contained in prime list.
#   This reduces a loop to check if all the values in the list of rotations are
#   in the list of primes

from helperFunctions import *

def CircularPrimes(n):
    primes = set(SOE(n))           #Point 1
    circularPrimes = []
    for prime in primes:
        if prime<10:circularPrimes.append(prime)   #Point 2
        elif prime not in circularPrimes:          #Point 3
            digitRotations = set([])
            lst = map(int,str(prime))
            if any(i%2==0 for i in lst):continue   #Point 4
            for i in range(len(lst)):
                lst.append(lst.pop(0))
                nextRotation = lst 
                digitRotations.add(int(''.join(map(str,nextRotation))))
            if not digitRotations - primes:        #Point 5
                circularPrimes.extend(digitRotations)
    return circularPrimes

if __name__ == "__main__":
    print(len(CircularPrimes(1000000)))

"""
ALTERNATE SOLn(Very Similar)

1) Get the single digit ones directly.
2) We know that the numbers have to end in 1,3,7,9 (except for the single digit ones). Also, all primes are of the form 
   6n-1 or 6n+1. Therefore, given an ending digit and the reminder when divided by 6, we can find all the possible ending digits
   that can be prime in a decade. For example, if you divide 11 by 6, it gives a reminder of 5. This means, than 11 is of the form
   6n-1. Therefore, possible primes are 11,13,17,19. I leave it upto the reader to figure out the other possibilities. 
3) Once you have seen a sequence with a given first digit, you never have to use that digit again for a given number of digits in a number.
For example, for 2 digit numbers, once you have finished 11 to 19, you never have to use 1 again because you have seen all 2 digit numbers
that contain a 1 and can possibly be prime.

"""
