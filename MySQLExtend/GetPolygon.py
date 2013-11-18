# -*- coding:utf-8 -*-
import Config
import re
from decimal import *
from shapely.geometry import Polygon
import Module.PySql as PySql
# use this, brew install geos / sudo apt-get install libgeos-dev

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
		result.append(
			dict(idx = row[0], name = row[1], address = row[2])
		)

	return result

def searchByIdx( idx ) :
	x.execute("""SELECT AsText(`geo`) FROM `siblo_locations` WHERE `id` = %s""", (idx, ))

	rows = x.fetchall()
	if len(rows) == 0 :
		return None

	return parseGeometry(rows[0][0])



if __name__ == "__main__" : #37.556962009064506 127.06838607788086 
	print( searchFromPolygon( str(37.556962009064506), str(127.06838607788086) ) )
