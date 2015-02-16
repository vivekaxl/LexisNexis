class Close:
  def __init__(i, goal=0.03, enough=25, head=None):
    i.goal = goal
    i.head = i if head==None else head
    i.samples, i.enough, i.all, i.m  = [],enough,0,0
    i.head,    i.median, i.after  = None, None, None
  def log(i,x, before=0.0):
    i.head.all += 1
    i.m += 1
    before += i.m
    n = len(i.samples)
    if n >= i.enough:
      i.samples  = sorted(i.samples)
      i.median   = i.samples[n // 2]
      i.after    = Close(head=i.head)
    else:
      i.samples += [x]
    if (1 - before/i.head.n) < i.head.goal:
      return True
    else:
      if i.median != None and x < i.median:
        i.after.log(before)
      
        
