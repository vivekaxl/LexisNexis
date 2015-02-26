#Brute Force - ~5s
from helperFunctions import *

def triangleNumber(n):
    i=1
    num = 0
    while True:
       num = num+i
       if len(factors(num))>n:
           return num
       i+=1
        
print triangleNumber(500)
