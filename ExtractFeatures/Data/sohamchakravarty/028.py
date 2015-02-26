N = 1001
print sum([j for i in xrange(3,N+1,2) for j in xrange((i-2)**2,(i**2),i-1)]) + N*N

