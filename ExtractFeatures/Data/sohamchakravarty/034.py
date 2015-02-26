def DigitFactorials():
   sum1=0
   for y in range(11,10000000):
      if y==sum([reduce(int.__mul__,range(1,x+1),1) for x in map(int,str(y))]):
         sum1+= y
   return sum1

print DigitFactorials()

"""
#Other soln
fact = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880)

def sum_of_digits_factorial(n):
   s = 0
   while n > 0:
      d = n % 10
      s = s + fact[d]
      n = n / 10
   return s

print sum(n for n in xrange(10, 10000000) if n == sum_of_digits_factorial(n))
"""



