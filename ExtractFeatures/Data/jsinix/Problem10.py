# Question: Summation of primes
# Problem 10
# The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
# Find the sum of all the primes below two million.
# Answer: 142913828922


#!/usr/bin/python
def is_prime(num):
    for j in range(2,num):
        if (num % j) == 0:
            return False
    return True

list1 = []
for i in range(3,2000000,2):
    if is_prime(i) == True:
        list1.append(i)

sum1 = 0
for j in list1:
    sum1 = sum1+j

print sum1
