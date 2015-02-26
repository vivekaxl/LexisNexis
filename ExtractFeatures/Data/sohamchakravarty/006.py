sum1 = sum([x**2 for x in range(1,101)])
sum2 = (sum([x for x in range(1,101)]))**2

print sum2 - sum1
