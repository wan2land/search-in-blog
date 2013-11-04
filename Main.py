# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher

import Config

#1. instance = Searcher( name, **db_config )
Timer.checker()


inst = Searcher( "new", Config.fromJson("parallel.json") )
Timer.checker()

#for i in range(0, 100000) :
#	if i % 1000 == 0 :
#		Timer.checker()
#	

#2. instance.insert( Shapely, documents )
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "동해물과 백두산이 마르고 닳도록")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "하느님이 보우하사 우리나라 만세")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "꿈은 이루어질까")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "나의 세상 나의 마음")
Timer.checker()


#3. instance.search( type, Shapely, keyword = None )
result = inst.search("contains", Point(0,0).buffer(1), "꿈은" )
Timer.checker()


print result