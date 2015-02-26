def ReadFile(path,mode):
    fread=open(path,mode)
    filedata = fread.read().split(',')
    fread.close()
    return filedata

def NamesScores(names):
    scores = []
    count=1
    for name in names:
        name = eval(name)
        scores.append(count*sum([ord(i)-64 for i in name]))
        count+=1
    return scores

if __name__=="__main__":
    names = sorted(ReadFile('C:/Python27/Python Scripts/ProjectEuler Problems/Files/22. names.txt','r'))
    print sum(NamesScores(names))
