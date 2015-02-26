from helperFunctions import SOE

s = SOE(1000000)

sum = 0
lengthOfLongestSeries=0
requiredSum = 0
startIndex = 0
l=len(s)
for i in s[::-1]:
    if(s.index(i)<l/2):break
    startValue = int(i/2)
    while not s.count(startValue):
        startValue-=1
    index = s.index(startValue)        
    while index:      
        length=0
        sum = startValue
        while sum<i:
            index-=1
            sum+=s[index]
            length+=1
        if sum==i:
            if length>lengthOfLongestSeries:
                lengthOfLongestSeries = length
                requiredSum = i #requiredSum=sum
                startIndex = index
        if not index:break
        index = s.index(startValue)-1
        startValue = s[index]

    
        
print requiredSum

