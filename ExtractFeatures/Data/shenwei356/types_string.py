#!/usr/bin/env python3

f = 3.1415926
i = 1 << 30
s = 'hello,world'

print("{:.2f}".format(f))
print("{:.2%}".format(f/10))

print("{:=^79}".format("[ something ]"))

print("{} == {:,}".format(i, i))


s = "   >abcd   \r\n"
print("\t\n  ".isspace())
s = s.strip(" ")
print(s.upper())
print(s.lower())


s = "abcd  efg\t\taaa"
print(s.split())
print(s.split("\t"))
print(s.split(maxsplit=1))


