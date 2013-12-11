# -*- coding:utf-8 -*-
"""
python Test.py
실행시 일련의 과정이 순서대로 진행됩니다.

python Test.py story1 (기본값)
python Test.py story2
python Test.py story3
python Test.py story4

이런식으로 스토리 4개를 불러올 수 있습니다.
그러면 각 스토리에 맞춰 다음과 같은 서처를 생성합니다.
searcher = Searcher( "story1_"+str(option['count']), Config.fromJson("snb.json"), fulltext = False  )
스토리1~4는 fulltext사용 / 미사용, 분산 사용/미사용 으로 분류할 수 있습니다.
config파일안에서 서버를 한대 사용하면 그게 분산사용하지 않는 환경이기 때문에 config파일로 분류했습니다.

그 외에
python Test.py --only-init
python Test.py --only-insert
python Test.py --only-search

python Test.py --off-init
python Test.py --off-insert
python Test.py --off-search

이런 옵션들이 있습니다.

이 테스트는 서버접속 -> 데이터초기화 -> 데이터insert(RandomText를 사용) -> 데이터search의 과정으로 이루어져 있으며
각 결과를 출력하고 수행시간을 출력하도록 했습니다..

insert를 60만개 정도 하고 나면 굉장히 오랜 시간이 걸립니다. 만약 그 이후에 검색을 하는데 앞에 일련의 과정이 필요없다면
python Text.py --only-search 옵션을 통해 수행가능합니다. :)
"""

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
	"search" : True,
	"count" : 1000
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
	searcher = Searcher( "story1_"+str(option['count']), Config.fromJson("snb.json") )
elif option['story'] == 2 :
	searcher = Searcher( "story2_"+str(option['count']), Config.fromJson("snb.json"), fulltext = False )
elif option['story'] == 3 :
	searcher = Searcher( "story3_"+str(option['count']), Config.fromJson("onlyone.json") )
elif option['story'] == 4 :
	searcher = Searcher( "story4_"+str(option['count']), Config.fromJson("onlyone.json"), fulltext = False )

Timer.checker("Runtime")

#1. Data Initialize
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
	i_count = option['count']
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




