# Question: Largest palindrome product
# Problem 4
# A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
# Find the largest palindrome made from the product of two 3-digit numbers.
# Answer: 906609

#!/usr/bin/python
result = []
for i in range(999, 100, -1):
    for j in range(999, 100, -1):
	res = i*j
	if str(res) == str(res)[::-1]:
		result.append(res)
print max(result) 
