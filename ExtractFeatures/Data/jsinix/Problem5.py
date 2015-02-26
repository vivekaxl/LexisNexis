# Question: Smallest multiple
# Problem 5
# 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
# Answer: 232792560

#!/usr/bin/python
delta = 1
while (delta%1 != 0 or delta%2 != 0 or delta%3 != 0 or delta%4 != 0 or delta%5 != 0 or delta%6 != 0 or delta%7 != 0 or delta%8 != 0 or delta%9 != 0 or delta%10 != 0 or delta%11 != 0 or delta%12 != 0 or delta%13 != 0 or delta%14 != 0 or delta%15 != 0 or delta%16 != 0 or delta%17 != 0 or delta%18 != 0 or delta%19 != 0 or delta%20 != 0):
    delta = delta+1
print delta
