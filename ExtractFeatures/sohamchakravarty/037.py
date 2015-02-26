from helperFunctions import SOE

def TruncatablePrimes():
    primes = set(SOE(1000000))
    x = []
    count = 0
    for prime in primes:
        if prime<10:continue
        truncatedNums = set([prime])
        for i in range(1,len(str(prime))):
            truncatedNums.add(prime/10**i)
            truncatedNums.add(prime%10**i)
        if not truncatedNums - primes:
            x.append(prime)
            count+=1
        if count==11:
            break
    return x

print sum(TruncatablePrimes())
print time()-start
            
        
        
