import subprocess as subp

times = [12,24,50,100,200]

for time in times:
	print "====================================================================="
	cmd = "timeout %d python alternativeRig.py > %s.txt"%(time*60,time)
	try:
		subp.check_call(str(cmd), shell=True)
	except:
		pass