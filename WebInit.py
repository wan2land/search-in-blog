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

#docs = PySql.connect(host = "localhost", user = "root", password = "rooroo123", dbname="siblo")
#result = docs.query("""SELECT * FROM `blogorder`""")
"""
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

"""


#3. instance.search( type, Shapely, keyword = None )
result = searcher.search("disjoint", Point(0,0).buffer(1), u"영광".encode('utf-8'))

print result


