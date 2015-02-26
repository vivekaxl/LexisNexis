# Question: Multiples of 3 and 5
# Problem 1
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.
# Answer: 233168

#!/usr/bin/python
sum = 0
for i in range(0,1000):
    if i%3==0:
	sum = sum + i 
    elif i%5==0:
	sum = sum + i
print sum
