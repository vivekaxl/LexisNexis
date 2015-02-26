#!/usr/bin/env python3

# https://docs.python.org/3/library/functools.html
# https://docs.python.org/3/library/itertools.html
# https://docs.python.org/3/howto/functional.html

import itertools
import functools
import operator

l = (3, 4, 250, 6, 70, 40)
s = (0, 1, 0, 1, 0, 1)
b = 'ACTG'

print(list(itertools.accumulate(l, max)))

print(list(itertools.accumulate(l, operator.add)))
print(list(itertools.accumulate(l)))

print(list(itertools.accumulate(l, operator.add)))
print(list(itertools.accumulate(l)))

print('islice', list(itertools.islice(l, 3)), l[:3])
print('islice', list(itertools.islice(l, 1, 3)), l[1:3])
print('islice', list(itertools.islice(l, 1, None)), l[1:])


def compress(data, selectors):
    # compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F
    return (d for d, s in zip(data, selectors) if s)

print(list(itertools.compress(l, s)))

# print(list(itertools.cycle(l)))
print('originnal', l)
print('dropwhile', list(itertools.dropwhile(lambda x: x < 30, l))) # drop while !
print('takewhile', list(itertools.takewhile(lambda x: x < 30, l))) # take while !

print(list(itertools.filterfalse(lambda x: x < 30, l)))


print(list(itertools.permutations(b,2)))
print(list(itertools.combinations(b, 2)))
print(list(itertools.product(b, b.lower())))

print(list(itertools.repeat(b, 10)))


print(functools.reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]))


line_list = ['  line 1\n', 'line 2  \n']

# Generator expression -- returns iterator
stripped_iter = (line.strip() for line in line_list)

# List comprehension -- returns list
stripped_list = [line.strip() for line in line_list]