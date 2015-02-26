# example from  http://www.slideshare.net/gaetanlion/effect-size-presentation

pilot=[1,2,3,4,4,5]
control=[1,1,2,2,2,3,3,3,4,5]

#              control, pilot
def cliff(olds,news):
    gt = lt = 0.0
    for  new in news:
        for old in olds:
            if new > old: gt += 1
            if new < old: lt += 1
    return (gt - lt)/(len(olds) * len(news))

def fxsize(olds,news):
    ts=[(0.147,'small'),(0.5,'medium'),(0.8,'large')]
    c = cliff(olds,news)
    least,out = 10**32,ts[-1][1]
    for n,txt in ts:
        delta = abs(n-c)
        if delta < least:
            least,out=delta,txt
    return out

print fxsize(control,pilot)
                
                
