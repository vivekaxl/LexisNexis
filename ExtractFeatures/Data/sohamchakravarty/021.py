from helperFunctions import *

def AmicableNumbers(limit):
    nums = range(2,limit+1)
    amicables = []
    for i in nums:
        if not i:continue
        sumOfFactors1 = sum(factors(i))-i #removing N from the sum
        if sumOfFactors1!=i and sumOfFactors1<=limit and sumOfFactors1 in nums:
            value = nums[sumOfFactors1-2]
            sumOfFactors2 = sum(factors(value))-value
            if sumOfFactors1==value and sumOfFactors2==i:
                amicables.append([i,value])
                nums[i-2] = 0
                nums[value-2] = 0
    return amicables

if __name__=="__main__":
    amicables = AmicableNumbers(10000)
    sumOfNums = sum([sum(i) for i in amicables])
    print sumOfNums
