#Function to check if both bases of 'x' are palindromic
def isPalindrome(x):
    dec = str(x)
    binary =  bin(x).replace('0b','')
    if dec==dec[::-1] and binary==binary[::-1]:
        return True
    return False

def main():
    limit = 1000000
    
    nums = []
    
    for i in xrange(1,len(str(limit))):  #As first palindrome is 11 - 2-digit
        if not i%2:                   #Even-digit
            nums.extend([j for j in xrange(10**(i-1)+1,10**i,11) if isPalindrome(j)])
        else:                         #Odd-digit
            nums.extend([j for j in xrange(10**(i-1),10**i) if isPalindrome(j)])
    
    print sum(nums)
    
    """
    nums1 = [i for i in xrange(1,10) if isPalindrome(i)] #1-digit
    nums2 = [i for i in xrange(11,100,11) if isPalindrome(i)] #2-digit
    nums3 = [i for i in xrange(101,1000) if isPalindrome(i)]  #3-digit
    nums4 = [i for i in xrange(1001,10000,11) if isPalindrome(i)] #4-digit
    nums5 = [i for i in xrange(10001,100000) if isPalindrome(i)]  #5-digit
    nums6 = [i for i in xrange(100001,1000000,11) if isPalindrome(i)] #6-digit
    print nums1,nums2,nums3,nums4,nums5,nums6
    """

if __name__=="__main__":
    main()

"""
#ANOTHER SOLn
#~802ms
sum = 0
for i in range(1,1000000):
    if str(i) == str(i)[::-1] and bin(i)[2:] == bin(i)[2:][::-1]:
        sum += i

print sum

"""
