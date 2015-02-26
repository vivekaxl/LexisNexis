def Fib(digit):
    a,b,i = 1,2,3
    while True:
        if digit==len(str(b)):
            return i
        a,b,i = b,a+b,i+1

if __name__=="__main__":
    print Fib(1000)
