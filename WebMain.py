# -*- coding:utf-8 -*-
import Config
import Module.Timer as Timer

from flask import Flask
from flask import render_template, request, jsonify
from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
from Module.Formula import parser as fpaser
from Web.CrossdomainAllow import crossdomain
from MySQLExtend.GetPolygon import searchFromAll, searchByIdx, parseGeometry
from Jamo import divText
from Geo.Converter import text2geo, geo2text



app = Flask(__name__)
searcher = None
searcher = Searcher( "blogs", Config.fromJson("web.json"), fulltext = False)

#url_for("static", filename="style.css")

def retError() :
	return jsonify( result = False )	

def procFormula( formula ) :
	indexes, operators = fpaser( formula )

	print indexes, operators

	polygon = []
	for index in indexes :
		polygon.append( text2geo(searchByIdx(index)) )

	result = polygon[0]
	i = 0
	for operator in operators :
		if operator == '+' :
			result = result.union( polygon[i+1] )
		elif operator == '-' :
			result = result.difference( polygon[i+1] )
		elif operator == '*' :
			result = result.intersection( polygon[i+1] )
		i = i+1

	return result


@app.route("/")
@app.route("/<title>")
def hello(title = "hello") :
	return render_template('index.html', title=title)





@app.route("/ajax/searchAddress", methods=['GET'])
@crossdomain(origin='*')
def ajaxSearchAddress() :

	keyword = request.args.get("keyword", None)

	if keyword is None or keyword == '' :
		return retError()

	result = searchFromAll( "".join( divText( keyword ) ).encode('utf-8') )

	if isinstance(result, (list, tuple)) and len(result) == 0 :
		return retError()

	return jsonify( result = result )







@app.route("/ajax/getPolygon", methods=['GET'])
@crossdomain(origin='*')
def ajaxGetPolygon() :

	formula = request.args.get("formula", None)

	result = procFormula(formula)

	return jsonify( result = geo2text(result) )



@app.route("/ajax/searchResult", methods=['GET'])
@crossdomain(origin='*')
def ajaxSearchResult() :

	formula = request.args.get("formula", None)
	keyword = request.args.get("keyword", None)
	operator = request.args.get("operator", None)

	if keyword is None or keyword == '' :
		keyword = None

	if isinstance(keyword, unicode) :
		keyword = keyword.encode("utf-8")

	polygon = procFormula(formula)

	print keyword
	
	result = searcher.search(operator, polygon, keyword, option="all")

	#print ([(item[0],item[2]['title'],item[2]['url']) for item in result[0:10]])
	#if isinstance(result, (list, tuple)) and len(result) == 0 :
	#	return retError()

	return jsonify( result = [(item[0],item[2]['title'],item[2]['url']) for item in result] )


@app.errorhandler(404)
def not_found(error):
    return "404 error..", 404



if __name__== "__main__" :
	app.run(debug=True)