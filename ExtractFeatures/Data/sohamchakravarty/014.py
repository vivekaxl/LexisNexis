def CollatzSequence(N):
    seq = []
    nextCollatz = lambda x:3*x+1 if x%2 else x/2
    i = N
    if i%2:
        while i!=1:
            seq.append(i)
            i = nextCollatz(i)
    seq.append(1)
    return seq

def LongestCollatzSequence(N):
    length = 0
    val = 0
    for i in xrange(1,N,2):
        tmp = CollatzSequence(i)
        if length<len(tmp):
            length = len(tmp)
            val = tmp[0]
    return val
        
print LongestCollatzSequence(1000000)
