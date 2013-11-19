# -*- coding:utf-8 -*-
# Fultext O distritution O

import sys
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
import Config

option = {
	"story" : 1,
	"init" : True,
	"insert" : True,
	"search" : True
}

if len(sys.argv) < 2 :
	print "Run as Default Option!"
else :
	if sys.argv[1] == 'story2' :
		option['story'] = 2
	elif sys.argv[1] == 'story3' :
		option['story'] = 3
	elif sys.argv[1] == 'story4' :
		option['story'] = 4

	if '--only-search' in sys.argv :
		option['init'] = False
		option['insert'] = False
	elif '--only-init' in sys.argv :
		option['insert'] = False
		option['search'] = False
	elif '--only-insert' in sys.argv :
		option['init'] = False
		option['search'] = False

	if '--off-init' in sys.argv :
		option['init'] = False
	if '--off-insert' in sys.argv :
		option['insert'] = False
	if '--off-search' in sys.argv :
		option['search'] = False


#0. Connect Server!!
print "Use choose Story", option['story']
print "Connecting Server..."
Timer.start()
if option['story'] == 1 :
	searcher = Searcher( "story1", Config.fromJson("snb.json") )
elif option['story'] == 2 :
	searcher = Searcher( "story2", Config.fromJson("snb.json"), fulltext = False )
elif option['story'] == 3 :
	searcher = Searcher( "story3", Config.fromJson("onlyone.json") )
elif option['story'] == 4 :
	searcher = Searcher( "story4", Config.fromJson("onlyone.json"), fulltext = False )
Timer.checker("Runtime")


if option['init'] :
	print "모든 데이터를 초기화 합니다. 정말로 실행하시겠습니까..?"
	check = raw_input("(y/n) =>")
	if check != 'y' :
		exit()

	Timer.start()

	searcher.destroy()
	searcher.init()

	Timer.checker("")




#2. instance.insert( Shapely, documents )
if option['insert'] :
	i_count = 10000
	print "데이터를 색인합니다. 16 *", i_count ,"=", (i_count * 16) ,"개의 문서."

	rt = RandomText() #Random Text Creator

	Timer.start()

	for i in range(0, i_count) :
		searcher.insert( 
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate()),
			( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate())
		)
		sys.stdout.write('\r')
		sys.stdout.write("[%-20s] %d%%" % ('='*( (i*20) //i_count), i*100//i_count))
		sys.stdout.flush()
	sys.stdout.write('\r')
	sys.stdout.write("[%-20s] %d%%\r\n" % ('='*20, 100))
	Timer.checker()



#3. instance.search( type, Shapely, keyword = None )
if option['search'] :
	print "검색을 실행합니다. "

	Timer.start()

	result = searcher.search("contains", Point(0,0).buffer(200), "lorem ipsum")
	print "Found!", result

	Timer.checker()




