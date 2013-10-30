# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbLibrary import Searcher


import Config

#1. instance = Searcher( name, **db_config )
Timer.checker()


inst = Searcher( "new", **Config.fromJson("mysql.json") )
Timer.checker()

#for i in range(0, 100000) :
#	if i % 1000 == 0 :
#		Timer.checker()
#	

#2. instance.insert( Shapely, documents )
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "동해물과 랄라랄라 음")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) , "블라블라 랄라랄라 음하하하")
#inst.insert( Point(randint(-2500,2500),randint(-2500,2500)).buffer(randint(1,3)) )
Timer.checker()


#3. instance.search( type, Shapely, keyword = None )
result = inst.search("disjoint", Point(0,0).buffer(1), "동해물과 랄라랄라" )
Timer.checker()


print result