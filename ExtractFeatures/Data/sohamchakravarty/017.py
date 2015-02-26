#A generalized approach

def NumberLetterCount(startValue,endValue):
    referDict = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",
                 11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",19:"nineteen",20:"twenty",
                 30:"thirty",40:"forty",50:"fifty",60:"sixty",70:"seventy",80:"eighty",90:"ninety",100:"hundred",1000:"thousand"}

    letterCounts = 0
    largestNDigitWordCounts = [0]  #largestNthDigitWordCounts[1] stores wordCounts from 1-9(9 largest 1 digit num) = 36,
                                   #largestNthDigitWordCounts[2] stores wordCounts from 1-99(99 largest 2 digit num) = 854,...
    tensMultiplesWordCount = 0
    i=startValue
    while True:
        if i<20:
            letterCounts += len(referDict[i])
            if i==9: largestNDigitWordCounts.append(letterCounts)
            i+=1
            continue
        digitCount = len(str(i))      #number of digits in i
        keyValue = 10**(digitCount-1) #the multiplying factor
        if i==keyValue:               #if i is 10,100,1000...
            tensMultiplesWordCount = len(referDict[keyValue])
        if i==endValue:
            return (letterCounts + len(referDict[i/keyValue]) + tensMultiplesWordCount)
        if i<100:                     #for numbers 10,20,30,...
            baseNumberWordCount = len(referDict[i])
        else:                         #numbers above 100 start with 'one','two' and 'three'
            baseNumberWordCount = len(referDict[i/keyValue])
        letterCounts += (baseNumberWordCount * keyValue) + (tensMultiplesWordCount * keyValue) + largestNDigitWordCounts[digitCount-1]
        if i>=100: letterCounts += len("and") * (keyValue-1)
        if i==(keyValue*10)-keyValue:  #if i is 90,900,...
            largestNDigitWordCounts.append(letterCounts)
        i+=keyValue


if __name__=="__main__":
    print(NumberLetterCount(1,1000))
