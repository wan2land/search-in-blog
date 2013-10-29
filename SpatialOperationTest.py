# -*- coding:utf-8 -*-
import SnbLibrary
import time
import geoConverter
""" 다 필요 없는 코드임, 테스트 하기 위해 만듬 """
conn = SnbLibrary.connect(user="root", password="1234", host = '127.0.0.1', port = 3307 ,database='test')
my_table = conn.selectTable('geom')
result = my_table.searchBySpatial()

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon

def text2geoTest() :
	num = 0
	for geom in result:
		geom = str(result[num])
		p = geoConverter.text2geo(geom)
		print p
		if num == len(result) :
			break
		num = num + 1
	print "------------------------------------------------------"
	
def totalPrint() :
	num = 0
	for geom in result:
		geom = str(result[num])
		geom = geom.replace(".0000000000000000","")
		print (" %d, %s, Area: %f" %(num, geom, result[num].area))
		if num == len(result) :
			break
		num = num + 1
	print ""

def easyPrint(num1,op,num2) :
	if op == "union" :
		geom = result[num1].union(result[num2])
	if op == "difference" :
		geom = result[num1].difference(result[num2])
	if op == "intersection" :
		geom = result[num1].intersection(result[num2])
	if op == "intersects" :
		geom = result[num1].intersects(result[num2])
	if op == "disjoint" :
		geom = result[num1].disjoint(result[num2])
	if op == "within" :
		geom = result[num1].within(result[num2])
	if op == "contains" :
		geom = result[num1].contains(result[num2])
	if op == "touches" :
		geom = result[num1].touches(result[num2])
	if op == "equals" :
		geom = result[num1].equals(result[num2])	
	
	geomText = str(geom).replace(".0000000000000000","")

	if op == "union" or op == "difference" or op == "intersection" :
		geomarea = geom.area
		print (" %d %s %d \t: %s, Area: %d" %(num1, op, num2, geomText, geomarea))
	else :
		print (" %d %s %d \t: %s" %(num1, op, num2, geomText))

def totalAnalyzer (op) :
	numlist_1 = [0,1,2,3,4,7,8,9,10,11]
	op_1 = ["union","difference","intersection"]
	numlist_2 = [0,1,2,3,4,5,6,7,8,9,10,11]
	op_2 = ["intersects","disjoint","within","contains","touches","equals"]
	"""
	if op == "union" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,7,8,9,10] #5,6,11
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10] #6,11
			elif e == 5 :
				numlist_1 = [2,4,5,8,10] #0,1,3,6,7,9,11
			elif e == 6 :
				numlist_1 = []	#다안됨
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 11 :
				numlist_1 = [0,2,3,7,8,9,10,11] #1,4,5,6
					
			for x in numlist_1 :
				easyPrint(e,op,x)
	"""
	if op == "union" :
		numlist_1 = [0,1,2,3,4,5,6]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
			elif e == 6 :
				numlist_1 = [0,1,2,3,4,5,6] #5,6
					
			for x in numlist_1 :
				easyPrint(e,op,x)


	if op == "intersection" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,8,9,10,11]	#5,6,7
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,7,8,9,10]	#5,6,11
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11]	#5,6
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10] #6,11
			elif e == 5 :
				numlist_1 = [2,4,5,8,10,11] #0,1,3,6,7,9
			elif e == 6 :
				numlist_1 = [] #다안됨
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 11 :
				numlist_1 = [0,2,5,7,8,9,10,11]	#1,3,4,6
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "difference" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11]	#5,6안됨
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,7,8,9] #5,6,10,11
			elif e == 2 :
				numlist_1 = [0,2,3,4,5,7,8,9,10,11] #1,6
			elif e == 3 :
				numlist_1 = [0,2,3,7,8,9,10] #1,4,5,11
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10] #6,11
			elif e == 5 :
				numlist_1 = [] #다안됨
			elif e == 6 :
				numlist_1 = [] #다안됨
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,7,8,9,10,11] #5,6
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 11 :
				numlist_1 = [0,2,3,7,8,9,10,11] #1,4,5,6
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "intersects" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 6 :
				numlist_1 = [0,2,3,6,7,9,10] #1,4,5,8,11
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "disjoint" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 6 :
				numlist_1 = [0,2,3,6,7,9,10]	#1,4,5,8,11
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
					
			for x in numlist_1 :
				easyPrint(e,op,x)				

	if op == "within" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 6 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "contains" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 6 :
				numlist_1 = [0,1,2,3,5,6,7,8,9,10,11] #4
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "touches" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11]	#6
			elif e == 6 :
				numlist_1 = [0,2,3,6,7,9,10]	#1,4,5,8,11
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,7,8,9,10,11] #6
					
			for x in numlist_1 :
				easyPrint(e,op,x)

	if op == "equals" :
		numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
		for e in numlist_1 :
			if e == 0 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 1 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 2 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 3 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 4 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 5 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 6 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 7 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 8 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 9 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 10 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
			elif e == 11 :
				numlist_1 = [0,1,2,3,4,5,6,7,8,9,10,11]
					
			for x in numlist_1 :
				easyPrint(e,op,x)

""" -------------------------------------------------- """
text2geoTest()
totalPrint()
#totalAnalyzer("union")
#totalAnalyzer("intersection")
#otalAnalyzer("")
#print 201 % 11

#print 'running time : ' + str( float( int(round(time.time() * 1000)) - start ) / 1000 )
"""
SET @g = 'POINT(1 1)';
INSERT INTO geom VALUES (PointFromText(@g));

SET @g = 'LINESTRING(0 0,1 1,2 2)';
INSERT INTO geom VALUES (LineStringFromText(@g));

SET @g = 'POLYGON((0 0,10 0,10 10,0 10,0 0),(5 5,7 5,7 7,5 7, 5 5))';
INSERT INTO geom VALUES (PolygonFromText(@g));

SET @g =
'GEOMETRYCOLLECTION(POINT(1 1),LINESTRING(0 0,1 1,2 2,3 3,4 4))';
INSERT INTO geom VALUES (GeomCollFromText(@g));
"""