from math import sqrt
from itertools import permutations

def SOE(startValue,endValue):
    primes = list(range(startValue,endValue+1))
    for i in xrange(2, int(sqrt(endValue))+1):   #n^0.5 => O(log logN)
        primes = filter(lambda x: x==i or x%i,primes)  #O(N)
    return primes

def main(): 
    primes = set(SOE(1488,9999))
    diff = 3330
    for prime in primes:
        x = set([prime,prime+diff,prime+diff*2])
        perms = set([int(''.join(i)) for i in permutations(str(prime))])
        if not x - primes and not x - perms:
            print x
            break
            
if __name__=="__main__":
    main()


"""
Up to 5 digits:

i=1487 j=4817 k=8147 Difference: 3330
i=2969 j=6299 k=9629 Difference: 3330
i=11483 j=14813 k=18143 Difference: 3330
i=11497 j=41719 k=71941 Difference: 30222
i=12713 j=13217 k=13721 Difference: 504
i=12739 j=17239 k=21739 Difference: 4500
i=12757 j=17257 k=21757 Difference: 4500
i=12799 j=17299 k=21799 Difference: 4500
i=14821 j=48121 k=81421 Difference: 33300
i=14831 j=31481 k=48131 Difference: 16650
i=14897 j=47189 k=79481 Difference: 32292
i=18503 j=51803 k=85103 Difference: 33300
i=18593 j=51893 k=85193 Difference: 33300
i=19543 j=35491 k=51439 Difference: 15948
i=20161 j=20611 k=21061 Difference: 450
i=20353 j=25303 k=30253 Difference: 4950
i=20359 j=25309 k=30259 Difference: 4950
i=20747 j=24077 k=27407 Difference: 3330
i=23887 j=28387 k=32887 Difference: 4500
i=25087 j=52807 k=80527 Difference: 27720
i=25793 j=59273 k=92753 Difference: 33480
i=25913 j=39521 k=53129 Difference: 13608
i=25981 j=59281 k=92581 Difference: 33300
i=26317 j=31267 k=36217 Difference: 4950
i=26597 j=59627 k=92657 Difference: 33030
i=28933 j=29383 k=29833 Difference: 450
i=29669 j=62969 k=96269 Difference: 33300
i=31489 j=34819 k=38149 Difference: 3330
i=31489 j=39841 k=48193 Difference: 8352
i=32969 j=63299 k=93629 Difference: 30330
i=34961 j=39461 k=43961 Difference: 4500
i=35407 j=40357 k=45307 Difference: 4950
i=35491 j=39541 k=43591 Difference: 4050
i=35671 j=53617 k=71563 Difference: 17946
i=37561 j=51637 k=65713 Difference: 14076
i=49547 j=54497 k=59447 Difference: 4950
i=55603 j=56053 k=56503 Difference: 450
i=60373 j=63703 k=67033 Difference: 3330
i=60757 j=65707 k=70657 Difference: 4950
i=61487 j=64817 k=68147 Difference: 3330
i=62597 j=65927 k=69257 Difference: 3330
i=62773 j=67723 k=72673 Difference: 4950
i=63499 j=63949 k=64399 Difference: 450
i=67829 j=68279 k=68729 Difference: 450
i=68713 j=78163 k=87613 Difference: 9450
i=71947 j=74719 k=77491 Difference: 2772
i=73589 j=78593 k=83597 Difference: 5004
i=76717 j=77167 k=77617 Difference: 450
i=76819 j=81769 k=86719 Difference: 4950
i=78941 j=84179 k=89417 Difference: 5238
i=80191 j=89101 k=98011 Difference: 8910
i=83987 j=88937 k=93887 Difference: 4950
i=88937 j=93887 k=98837 Difference: 4950
i=89387 j=93887 k=98387 Difference: 4500
i=92381 j=92831 k=93281 Difference: 450
"""
    
    
