#!/usr/bin/env python3
import re

s = ">id=12345 abc=123 ABCd="

pattern = re.compile('([\w]+)=([^ =]+) *')

p2 = re.compile('ABC')

print(p2.search(s).group())

print(p2.search(s, re.IGNORECASE).group())  # re.IGNORECASE did not works
print(re.search('ABC', s, re.IGNORECASE).group())
print(re.search('(?i)ABC', s).group())  # better

print(re.sub('(?i)(ABC)', '\g<1>\g<1>', s))  # ugly backreferences

print('=' * 79)

#

print(re.split('\s+', s))



# ===============================================================================


all = pattern.findall(s)  # list
print(all)

d = [{x[0]: x[1]} for x in all]
print(d)

d2 = dict(all)
print(d2)

d3 = {}
for x in all:
    d3[x[0]] = x[1]
print(d3)
