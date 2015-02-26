print str(sum(i**i for i in xrange(1,1001)))[-10:]

"""
#Another Solution
print sum(x ** x for x in range(1, 1001)) % (10 ** 10)

"""

