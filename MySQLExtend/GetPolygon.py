# -*- coding:utf-8 -*-
import Config
import re
from decimal import *
from shapely.geometry import Polygon
import Module.PySql as PySql

"""
해당 모듈을 사용하기 위해서는 
맥의 경우 brew install geos
리눅스의 경우 sudo apt-get install libgeos-dev
를 설치하고 난 후 사용할 수 있다.

물론 shapely 설치는 기본..

이 모듈은 웹에서 주소 입력할 때 해당하는 폴리곤을 검색하는 것. 초반에는 전체 함수 의존도가 컸으나
이후에는 다른 더 좋은 잘 짠 소스로 대체되면서 searchFromAll, searchByIdx, parseGeometry
요거 3개의 메서드만 사용하게 됨.
사실 parseGeometry의 경우도 Geo.Converter 모듈이 더 사용하기 좋음.
"""

conn = PySql.connect( **Config.fromJson("snb.json")[0] ).getConnector()

x = conn.cursor()
x.execute("SET NAMES utf8")

def str2geometry( geometry ) :
	if geometry is None :
		return False

	m = re.search('^(\w+)', geometry)
	shape = m.group(0)

	if shape == "POLYGON" :
		points = []
		temp = geometry[9:-2].split(",")
		for point in temp :
			x = point.split(" ")
			x[0] = Decimal(x[0])
			x[1] = Decimal(x[1])
			points.append( tuple(x) )
		return Polygon(points)
	else :
		return False
	return False

def parseGeometry( geometry ) :
	if geometry is None :
		return False

	m = re.search('^(\w+)', geometry)
	shape = m.group(0)

	if shape == "POLYGON" :
		points = []
		temp = geometry[9:-2].split(",")
		for point in temp :
			points.append( point.split(" ") )
		return points
	else :
		return False
	return False

def searchFromPolygon( lat, lng ) :
	x.execute("""SELECT 'dong' as `where`, `idx`, `dong` as `name`, AsText(`polygon`) FROM `sib_dong_t`
		WHERE `latmin` < %s AND `latmax` > %s AND `lngmin` < %s AND `lngmax` > %s""", 
		(lat, lat, lng, lng)
	)

	rows = x.fetchall()
	for row in rows :
		print str2geometry( row[3] )



def searchFromAll( text ) :
	key = text + '%'

	x.execute("""SELECT `id`, `name`, `address` FROM `siblo_locations` WHERE `keyword` LIKE %s LIMIT 0, 20""",
		(key, )
	)

	result = []
	rows = x.fetchall()
	for row in rows :
		print row

		print "-----"
		result.append(
			dict(idx = row[0], name = row[1], address = row[2])
		)

	return result

def searchByIdx( idx ) :
	x.execute("""SELECT AsText(`geo`) FROM `siblo_locations` WHERE `id` = %s""", (idx, ))

	rows = x.fetchall()
	if len(rows) == 0 :
		return None

	return (rows[0][0])



if __name__ == "__main__" : #37.556962009064506 127.06838607788086 
	print( searchFromPolygon( str(37.556962009064506), str(127.06838607788086) ) )
