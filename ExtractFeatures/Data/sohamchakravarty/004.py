from helperFunctions import *

#Function to extract 3-digit factors from list of all factors
def extractFactors(factors,digitCount):
    for x in factors:                      #O(log logN) if N is a list of all 6 digit numbers
        if len(str(x))==digitCount:
            yield x

#Function to check if a required palindrome exists
def findLargestPalindrome(start,end,numberOfDigits):
    for x in xrange(start,end,-1):     #O(N)
            num = map(int,str(x))
            if num == num[::-1]:       #if x is palindrome
                f = sorted(extractFactors(factors(x),numberOfDigits),key=int,reverse=True)   #descending order of 3-digit factors
                if(len(f)>=2):
                    for i in f[::2]:
                        if f.index(i)!=len(f)-1:
                             product = i*f[f.index(i)+1]
                             if product<x : break             #as the list is sorted, the product will always decrease
                             if product == x:
                                 return x

if __name__=="__main__":
    numberOfDigits = 3
    #Get the Largest numberOfDigits*2(3*2=6) digits Palindrome possible
    start = convertListToInt([9]*numberOfDigits)**2 #999*999
    end = convertListToInt([1]*numberOfDigits) #111111 <- smallest palindrome
    print(findLargestPalindrome(start,end,numberOfDigits))

#Efficieny : O(N log (logN)^3) or O(N 3log logN)
