print sum(int(digit) for digit in str(reduce(lambda x,y:x*y,[x for x in range(1,101)])))

