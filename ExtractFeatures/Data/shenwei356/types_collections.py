#!/usr/bin/env python3

from collections import *

cnt = Counter()

for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1

print(cnt['red'])

q = deque(('a', 'b'))

q.append('c')
q.extend(('a', "我"))
q.extendleft((0, 1))
print(q)

d = {}
d.setdefault("a",[]).append(1)
print(d)
d.setdefault("a",[]).append(1)
print(d)