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
		"nodata"
		return 0
	return p

def convertGeometryCollection(text) :
	geom = text.replace(",POINT","|POINT")
	geom = geom.replace(",LINESTRING","|LINESTRING")
	geom = geom.replace(",POLYGON","|POLYGON")
	geom = geom.replace(",MULTIPOINT","|MULTIPOINT")
	geom = geom.replace(",MULTILINESTRING","|MULTILINESTRING")
	geom = geom.replace(",MULTIPOLYGON","|MULTIPOLYGON")
	geom = geom.replace(",GEOMETRYCOLLECTION","|GEOMETRYCOLLECTION")
	
	start = geom.find("(")
	end = len(geom)
	geom = Substr(geom,start+1,end-1)
	init = 0

	for word in geom.split("|") :		
		print word
		while(init == 0) :
			result = text2geo(word)
			init = 1
		p = text2geo(word)
		result = result.union(p)
	return result

def convertPoint(text) :
	result = []
	text = text.replace(" ",",")
	start = text.find("(")
	middle = text.find(",")
	end = text.find(")")
	lat = Substr(text,start+1,middle-1)
	lng = Substr(text,middle+1,end-1)
	tp = (float(lat),float(lng))
	result.append(tp)
	p = Point(result)
	return p

def convertLinestring(text) :
	start = text.find("(")
	end = text.find(")")
	geom = Substr(text,start+1,end-1)
	result = []
	for word in geom.split(",") :
		middle = word.find(" ")
		lat = Substr(word,0,middle-1)
		lng = Substr(word,middle+1,len(word))
		tp = (float(lat),float(lng))
		result.append(tp)
	p = LineString(result)
	return p

def convertPolygon(text) :
	start = text.find("((")
	end = text.find("))")
	div = text.find("),(")
	if start == -1 and end == -1 :
		geom = Substr(text,0,len(text))
	else :
		geom = Substr(text,start+2,end-1)
	if div == -1 :
		ext = []
		for word in geom.split(",") :
			middle = word.find(" ")
			lat = Substr(word,0,middle-1)
			lng = Substr(word,middle+1,len(word))
			tp = (float(lat),float(lng))
			ext.append(tp)
		p = Polygon(ext)

	else :	
		geom = geom.replace("),(","|")
		temp = geom.find("|")
		str_ext = Substr(geom,0,temp-1)
		str_int = Substr(geom,temp+1,len(geom))
		ext = []
		int = []
		for word in str_ext.split(",") :
			middle = word.find(" ")
			lat = Substr(word,0,middle-1)
			lng = Substr(word,middle+1,len(word))
			tp = (float(lat),float(lng))
			ext.append(tp)
		for word in str_int.split("|") :
			NotYetInt = []
			for smallword in word.split(",") :
				middle = smallword.find(" ")
				lat = Substr(smallword,0,middle-1)
				lng = Substr(smallword,middle+1,len(smallword))
				tp = (float(lat),float(lng))
				NotYetInt.append(tp)
			int.append(tuple(NotYetInt))
		p = Polygon(ext,int)
	if p.area > 0 :
		return p
	else :
		print ("Error : Sorry, Polygon must have an area < %s >" %(p))
		return 0	

def convertMultiPoint(text) :
	start = text.find("(")
	end = text.find(")")
	geom = Substr(text,start+1,end-1)
	result = []
	for word in geom.split(",") :
		middle = word.find(" ")
		lat = Substr(word,0,middle-1)
		lng = Substr(word,middle+1,len(word))
		tp = (float(lat),float(lng))
		result.append(tp)
	p = MultiPoint(result)
	return p

def convertMultiLineString(text) :
	start = text.find("((")
	end = text.find("))")
	geom = Substr(text,start+2,end-1)
	geom = geom.replace("),(","|")
	result = []
	NotYetresult = []
	for word in geom.split("|") :
		for smallword in word.split(",") :
			middle = smallword.find(" ")
			lat = Substr(smallword,0,middle-1)
			lng = Substr(smallword,middle+1,len(smallword))
			tp = (float(lat),float(lng))
			NotYetresult.append(tp)
		result.append(tuple(NotYetresult))
	p = MultiLineString(result)
	return p

def convertMultiPolygon(text) :
	start = text.find("(((")
	end = text.find(")))")
	geom = Substr(text,start+3,end-1)
	geom = geom.replace(")),((","%")
	result = []
	for poly in geom.split("%") :
		p = convertPolygon(poly)
		result.append(p)
	p = MultiPolygon(result)
	return p

def geo2text(geo) :
	if isinstance(geo,Point) or isinstance(geo,LineString) or isinstance(geo,Polygon) or isinstance(geo,MultiPoint)  or isinstance(geo,MultiLineString)  or isinstance(geo,MultiPolygon) :
		return str(geo)
	else :
		print "Sorry, It's not geometry type"
