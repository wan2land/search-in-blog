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
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "하느님이 보우하사 우리나라 만세")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "꿈은 이루어질까")


rt = RandomText()

Timer.checker()
"""

for i in range(0, 5) :
	inst.insertmany( 
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() ),
		( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , rt.generate() )
	)

Timer.checker()

"""
#3. instance.search( type, Shapely, keyword = None )
result = inst.search("disjoint", Point(0,0).buffer(200), "lorem" )
Timer.checker()


print result