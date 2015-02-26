
def prime(n):
    """ function that to get the prime number than < the input n
    """
    def z(x):
        if x :return True
        return False

    num1=range(0,n+1); 
    num2=int(n**0.5) +1
    #print 'num1 is:\n\n',num1
    for k in range(2,num2):
        num0=range(k,n+1,k);del num0[0]     
        for i in num0:
            num1[i]=0
    return filter(z, num1)


def prime2(n):
    def z(x):
        if z:
            return True
        return False

    num1=range(0,n+1)

if __name__=='__main__':
    print prime(102)
