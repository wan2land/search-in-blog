# -*- coding:utf-8 -*-
from time import time
"""
그냥 디버깅이랑 벤치마크 측정을 위한 모듈.
"""

gap = time()

def checker(msg = "Run..") :
	global gap
	now = time()
	print msg ,":", now - gap
	gap = now

def start() :
	global gap
	gap = time()