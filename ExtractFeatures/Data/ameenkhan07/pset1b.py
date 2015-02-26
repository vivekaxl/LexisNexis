b='bob'
v=0
for i in range(0,len(s)-2):
    x=0
    for j in range(0,len(b)):
        if s[i+j]==b[j]:
            x=x+1
            if x==len(b):
                v=v+1
print "Number of times bob occurs is: "+str(v)