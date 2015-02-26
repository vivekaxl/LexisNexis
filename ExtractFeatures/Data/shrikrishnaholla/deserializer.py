from itertools import *
def deserialize(filedb):
    """Read deserialized data from file"""
    details={}
    fo = open(filedb, "rb")
    stringdb=fo.read()
    beg=1
    end=0
    eof=stringdb.index("}}")
    while end!=eof:
        keylist=[]
        valuelist=[]                  
        end=beg+stringdb[beg:].index(": {")
        uname=stringdb[beg:end]
        uname=uname.strip("'")
        beg=end+3
        eor=stringdb[beg:].find("},")
        if eor==-1:
            eor=eof
        else:
            eor=beg+eor
        while end!=eor:
            end=beg+stringdb[beg:].index(':')
            key=stringdb[beg:end]
            key=key.strip("'")
            keylist.append(key)
            beg=end+2
            if  stringdb[beg]=='[':
                listlist=[]
                beg=beg+1
                listend=beg+stringdb[beg:].index(']')
                while end<listend:
                    end=stringdb[beg:listend].find(',')
                    if end==-1:
                        end=listend
                    else:
                        end+=beg
                    listvalue=stringdb[beg:end]
                    listvalue=listvalue.strip("'")
                    listlist.append(listvalue)
                    beg=end+2
                beg+=1
                valuelist.append(listlist)
            else:
                end=stringdb[beg:eor].find(',')
                if end==(-1):
                     end=eor
                else:
                     end+=beg
                value=stringdb[beg:end]
                value=value.strip("'")
                valuelist.append(value)
                beg=end+2
        beg+=1
        detail={}
        for k,v in izip_longest(keylist,valuelist):
            detail[k]=v
        details[uname]=detail                   
    fo.close()
    return details    