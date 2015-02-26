# Question: Special Pythagorean triplet
# Problem 9
# A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
# a2 + b2 = c2
# For example, 32 + 42 = 9 + 16 = 25 = 52.
# There exists exactly one Pythagorean triplet for which a + b + c = 1000.
# Find the product abc.
# Answer: a=200, b=375, c=425 Product: 31875000

#!/usr/bin/python

for a in range(1,1000):
    for b in range(a,1000):
        for c in range(b,1000):
            if (b > a):
                if (c > b):
                    if ((a*a) + (b*b) == (c*c)):
                        if (a+b+c) == 1000:
                            print "a=%s b=%s c=%s product: %s" % (a, b, c, a*b*c)
                            break
