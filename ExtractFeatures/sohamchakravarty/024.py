from itertools import permutations

if __name__=="__main__":
    #since digits range from 0...9, the number of permutation of digits possible is 10!
    x = list(permutations([0,1,2,3,4,5,6,7,8,9]))
    print int(''.join(map(str,x[1000000-1])))
    
