#!/usr/bin/env python3

bool_true = True
bool_false = False

if bool_true and not bool_false:
    print("true")

# http://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is-in-python
# is is for reference equality. Use it when you would like to know if two references refer to the same object
bool2 = bool_false
if bool2 is bool_false:
    print("same thing")

none = None
if not none:
    print("none")

#############################################

f = 0.5
i = 4
i2 = 10

print(f / i)
print(i / i2)
print(i // i2)  # floored quotient of x and y
print(i2 // i)
print(i % i2)
print(pow(10, 4))
print(2 ** 5)

#############################################

print(int("2"))
s = "3r"
try:
    print(int(s))
except ValueError:
    print("{} does not contain integer".format(s))

print(str(3))


#############################################
s = "123abcdefg"
print("abc" in s)
print(s)
for x in (s[1:], s[3:5], s[-3:-1]):
    i = s.index(x)
    print(' ' * i, x, ' ' * (len(s) - len(x) - i ), '$', sep='')