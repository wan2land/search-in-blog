# -*- coding:utf-8 -*-
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon

def Substr(str, start, stop) :
	return str[start:stop+1]

def text2geo(text) :
	print text
	if text.startswith("POINT") :
		p = convertPoint(text)
	elif text.startswith("LINESTRING") :
		p = convertLinestring(text)
	elif text.startswith("POLYGON") :
		p = convertPolygon(text)
	elif text.startswith("MULTIPOINT") :
		p = convertMultiPoint(text)
	elif text.startswith("MULTILINESTRING") :
		p = convertMultiLineString(text)
	elif text.startswith("MULTIPOLYGON") :
		p = convertMultiPolygon(text)
	elif text.startswith("GEOMETRYCOLLECTION") :
		p = convertGeometryCollection(text)
	else : 
		"Sorry, It's not geometry type"
		return 0
	return p

def geo2text(geo) :
	if isinstance(geo,Point) or isinstance(geo,LineString) or isinstance(geo,Polygon) or isinstance(geo,MultiPoint)  or isinstance(geo,MultiLineString)  or isinstance(geo,MultiPolygon) :
		return str(geo)
	else :
		print "Sorry, It's not geometry type"

def convertPoint(text) :
	basket = []
	head = text.find("(")
	geoString = Substr(text,head+1,len(text)-2) #geometry 좌표만 찾음
	pivot = geoString.find(" ")
	lat = Substr(geoString,0,pivot-1)
	lng = Substr(geoString,pivot+1,len(geoString))
	tp = (float(lat),float(lng))
	basket.append(tp)
	geo = Point(basket)
	return geo

def convertLinestring(text) :
	basket = []
	head = text.find("(")
	geoString = Substr(text,head+1,len(text)-2)	#geometry 좌표만 찾음
	for xy in geoString.split(",") :
		if xy.startswith(" ") :				#String -> Geometry -> String 변환 위해 필요
			blank = xy.find(" ")
			xy = Substr(xy, blank+1, len(xy))
		pivot = xy.find(" ")
		lat = Substr(xy,0,pivot-1)
		lng = Substr(xy,pivot+1,len(xy))
		tp = (float(lat),float(lng))
		basket.append(tp)
	geo = LineString(basket)
	return geo

def convertPolygon(text) :
	text = text.replace("), (","),(")
	head = text.find("((")
	tail = text.find("))")
	div = text.find("),(")

	if head == -1 and tail == -1 :	#Multipolygon인 경우
		geoString = text
	else :
		geoString = Substr(text,head+2,tail-1)

	if div == -1 :				# 구멍이 없는 경우
		ext = []
		for xy in geoString.split(",") :
			if xy.startswith(" ") :
				blank = xy.find(" ")
				xy = Substr(xy, blank+1, len(xy))
			pivot = xy.find(" ")
			lat = Substr(xy,0,pivot-1)
			lng = Substr(xy,pivot+1,len(xy))
			tp = (float(lat),float(lng))
			ext.append(tp)
		geo = Polygon(ext)

	else :						# 구멍이 있는 경우
		geoString = geoString.replace("),(","|")
		temp = geoString.find("|")
		extString = Substr(geoString,0,temp-1)
		intString = Substr(geoString,temp+1,len(geoString))
		ext = []
		int = []
		
		for xy in extString.split(",") :	# 외부 Polygon 
			if xy.startswith(" ") :
				blank = xy.find(" ")
				xy = Substr(xy, blank+1, len(xy))
			pivot = xy.find(" ")
			lat = Substr(xy,0,pivot-1)
			lng = Substr(xy,pivot+1,len(xy))
			tp = (float(lat),float(lng))
			ext.append(tp)
		
		for bigXy in intString.split("|") :		# 내부 Polygon
			basket = []
			for smallXy in bigXy.split(",") :
				if smallXy.startswith(" ") :
					blank = smallXy.find(" ")
					smallXy = Substr(smallXy, blank+1, len(smallXy))
				pivot = smallXy.find(" ")
				lat = Substr(smallXy,0,pivot-1)
				lng = Substr(smallXy,pivot+1,len(smallXy))
				tp = (float(lat),float(lng))
				basket.append(tp)
			int.append(tuple(basket))
		geo = Polygon(ext,int)
	if geo.area > 0 :
		return geo
	else :
		print ("Error : Sorry, Polygon must have an area < %s >" %(geo))
		return 0	

def convertMultiPoint(text) :
	head = text.find("(")
	tail = text.find(")")
	geoString = Substr(text,head+1,tail-1)
	basket = []
	for xy in geoString.split(",") :
		if xy.startswith(" ") :
			blank = xy.find(" ")
			xy = Substr(xy, blank+1, len(xy))
		pivot = xy.find(" ")
		lat = Substr(xy,0,pivot-1)
		lng = Substr(xy,pivot+1,len(xy))
		tp = (float(lat),float(lng))
		basket.append(tp)
	geo = MultiPoint(basket)
	return geo

def convertMultiLineString(text) :
	head = text.find("((")
	tail = text.find("))")
	geoString = Substr(text,head+2,tail-1)
	geoString = geoString.replace("),(","|")
	geoString = geoString.replace("), (","|")
	bigBasket = []
	for bigXy in geoString.split("|") :
		smallBasket = []
		for smallXy in bigXy.split(",") :
			if smallXy.startswith(" ") :
				blank = smallXy.find(" ")
				smallXy = Substr(smallXy, blank+1, len(smallXy))
			pivot = smallXy.find(" ")
			lat = Substr(smallXy,0,pivot-1)
			lng = Substr(smallXy,pivot+1,len(smallXy))
			tp = (float(lat),float(lng))
			smallBasket.append(tp)
		bigBasket.append(tuple(smallBasket))
	geo = MultiLineString(bigBasket)
	return geo

def convertMultiPolygon(text) :
	head = text.find("(((")
	tail = text.find(")))")
	geoString = Substr(text,head+3,tail-1)
	geoString = geoString.replace(")),((","%")
	geoString = geoString.replace(")), ((","%")
	basket = []
	for poly in geoString.split("%") :
		geo = convertPolygon(poly)
		basket.append(geo)
	geo = MultiPolygon(basket)
	return geo

def convertGeometryCollection(text) :
	geoString = text.replace(",POINT","|POINT")
	geoString = geoString.replace(",LINESTRING","|LINESTRING")
	geoString = geoString.replace(",POLYGON","|POLYGON")
	geoString = geoString.replace(",MULTIPOINT","|MULTIPOINT")
	geoString = geoString.replace(",MULTILINESTRING","|MULTILINESTRING")
	geoString = geoString.replace(",MULTIPOLYGON","|MULTIPOLYGON")
	geoString = geoString.replace(",GEOMETRYCOLLECTION","|GEOMETRYCOLLECTION")
	
	head = geoString.find("(")
	tail = len(geoString)
	geoString = Substr(geoString,head+1,tail-1)
	init = 0

	for divGeo in geoString.split("|") :
		while(init == 0) :
			geo = text2geo(divGeo)
			init = 1
		temp = text2geo(divGeo)
		geo = geo.union(temp)
	return geo
