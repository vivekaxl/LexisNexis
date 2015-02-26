def SpecialPythagorean():
    for a in xrange(1, 500):
     for b in xrange(a, 500):
         c = 1000 - a - b
         if c > 0:
             if c*c == a*a + b*b:
                 print a*b*c
                 break

if __name__=="__main__":
    SpecialPythagorean()
