from datetime import date

print sum(1 for y in xrange(1901,2001) for m in xrange(1,13) if date(y,m,1).strftime('%A')=='Sunday')

