from time import time

gap = None

def checker() :
	global gap
	if gap is None :
		gap = time()
		return

	now = time()
	print "Checker! : ", now - gap
	gap = now
