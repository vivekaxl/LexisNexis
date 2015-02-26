def DigitFifthPower():
   sum1=0
   for num in xrange(11,1000000):
      if num==sum([digit**5 for digit in map(int,str(num))]):
         sum1+=num
   return sum1

if __name__=="__main__":
   print DigitFifthPower()

