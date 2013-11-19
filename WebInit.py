# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
import Config
import Module.PySql as PySql

#Init
searcher = Searcher( "blogs", Config.fromJson("snb.json") )
#searcher.destroy()
#searcher.init()

docs = PySql.connect(host = "localhost", user = "root", password = "rooroo123", dbname="siblo")
result = docs.query("""SELECT * FROM `blogorder`""")

Timer.checker()


dummy = []
i = 0
for item in result.fetchall() :
	title = item[0]
	contents = item[2]
	latlng = Point(float(item[4]),float(item[3]))
	url = item[5]

	dummy.append( (latlng, contents, {
		'title' : title,
		'url' : url
	}) )

	if i % 30 == 0 :
		searcher.insert(*dummy)
		dummy = []
	i = i+1

Timer.checker()

#2. instance.insert( Shapely, documents )
"""
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
"""