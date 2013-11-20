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
	(Converter.text2geo("POLYGON((37.54015371921437 127.06276416778564,37.54685707459087 127.06654071807861,37.54597240231504 127.06937313079834,37.54682304892824 127.07018852233887,37.54794588759426 127.07031726837158,37.54729940679161 127.07413673400879,37.54576824568346 127.07735538482666,37.54512174599488 127.08246231079102,37.54311415859368 127.08134651184082,37.541753051638636 127.08168983459473,37.54127665833384 127.08306312561035,37.54001760423249 127.08246231079102,37.539098821605215 127.08065986633301,37.538145998033606 127.07709789276123,37.53545760874797 127.0762825012207,37.54015371921437 127.06276416778564))") ,"건대 건대입구 건대주변 건대맛집 으하하하 깔깔", {
		'title' : "건대주변",
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

