from math import sqrt

def PandigitalProducts():
    prods = []
    for num in range(1234,9876):
        factors = [i for i in range(1, int(sqrt(num)) + 1) if num % i == 0]
        digits = str(num)
        for m1 in factors:
            m2 = num/m1
            digits += str(m1) + str(m2)
            if '0' not in digits and len(digits)==len(set(digits))==9:
                prods.append(num)
                break
            digits = str(num)
    return prods
            
if __name__=="__main__":
    print sum(PandigitalProducts())


"""
Other Solns

#1) in ~5s
from itertools import permutations
s=[]
for i in permutations('123456789'):
   if int(i[0])*int(i[1]+i[2]+i[3]+i[4])==int(i[5]+i[6]+i[7]+i[8]) or int(i[0]+i[1])*int(i[2]+i[3]+i[4])==int(i[5]+i[6]+i[7]+i[8]):
      s.append(int(i[5]+i[6]+i[7]+i[8]))
print sum(set(s))

#2) in ~1s
def checkPan(x):
    t = []
    for i in range(1,10):
        a = x % 10
        x = x // 10
        if a in t:
            return False
        else:
            t.append(a)
    return True

prods = []
for m in range(2,100):
    newb = 123 if m > 9 else 1234
    newe = 10000 / ( m + 1 )

    for n in range(newb, newe):
        prod = m * n
        alln = str(m) + str(n) + str(prod)
        if int(alln) >= 123456789 and int(alln) < 987654322 and '0' not in alln:
            if checkPan(int(alln)):
                if prod not in prods:
                    prods.append(prod)

sum = 0
for i in prods:
    sum += i

print sum
"""
