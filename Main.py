# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
import Config

#1. instance = Searcher( name, **db_config )

inst = Searcher( "new", Config.fromJson("snb.json") )

#2. instance.insert( Shapely, documents )
#inst.destroy()
#exit()

rt = RandomText()

Timer.checker()

for i in range(0, 3) :
	inst.insert( 
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate(), {
			"foo" : "bar",
			"hello" : "world"
		}),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate(), {
			"num" : 123
		}),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate())

	)

Timer.checker()



#3. instance.search( type, Shapely, keyword = None )
result = inst.search("disjoint", Point(0,0).buffer(200), option="lorem")
Timer.checker()

for item in result :
	print item[1]
	if len(item) > 2 :
		print item[2]
