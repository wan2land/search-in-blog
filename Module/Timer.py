from time import time

gap = time()

def checker(msg = "Run..") :
	global gap
	now = time()
	print msg ,":", now - gap
	gap = now

def start() :
	global gap
	gap = time()