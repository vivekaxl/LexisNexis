sub=s[0]
l=s[0]
for i in range(1,len(s)):
	#if last letter is smaller than the current letter
	if sub[-1] <= s[i]:
		sub+=s[i]
	#else reset the sub string
	else :
		sub=s[i]
	#storing and resetting the substring such as to store the largest len
	if len(sub)>len(l):
			l=sub	
print l	
	
