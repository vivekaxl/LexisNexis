#!/usr/bin/env python3

a = ["abc", "cd", "我", "cd", "gfg"]
print(a)

a.sort()
print(list)

list2 = a.copy()
del list2[2]
list2.sort()
print(list2)

a.remove("我")

print(sorted(a, reverse=True))
print(sorted(a, key=len))
print(sorted(a, key=lambda x: 10 - len(x)))

sum = 0
for i in range(1, 10):
    print(i)
    sum = sum + i

print(sum)

print(range(1, 5))
a = list(range(1, 5))
print(a)

a = set(range(1, 5))
print(a)

b = {"a", "b"}

b.add("a")
print(b)

if "a" in b:
    print("in")

b.add("c")
print(b)

b.discard("a")
print(b)

b.discard("cc")
print(b)

a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
a == b == c == d == e

d = {'eggs': 212, 'sausage': 1, 'bacon': 1, 'spam': 500}

for k in sorted(list(d.keys()), key=lambda k: -d[k]):
    print("{}: {}".format(k, d[k]))

print("-" * 70)

del d['bacon']

if 'aaa' in d:
    del d['aaa']

for k, v in sorted(d.items()):
    print("{}: {}".format(k, v))
