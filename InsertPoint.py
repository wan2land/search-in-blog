# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
import Config
import Module.PySql as PySql

import Geo.Converter as Converter

#Init
searcher = Searcher( "blogs", Config.fromJson("web.json"), fulltext = False )
#searcher.destroy()
#searcher.init()

searcher.insert(
	(Converter.text2geo("POLYGON((37.58335766046065 126.97362899780273,37.575773270057695 126.97410106658936,37.57587530734239 126.97903633117676,37.576385491668546 126.97946548461914,37.57924245929811 126.97946548461914,37.580942983223 126.97998046875,37.58260945898645 126.97989463806152,37.58325563342967 126.97937965393066,37.58393581099492 126.97663307189941,37.58335766046065 126.97362899780273))") ,"경복궁 경복궁역 Dummy", {
		'title' : "경복궁",
		'url' : "http://wani.kr"
	})
)

exit()
docs = PySql.connect(host = "localhost", user = "root", password = "rooroo123", dbname="siblo")
result = docs.query("""SELECT * FROM `blogorder`""")

Timer.start()


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
"""

