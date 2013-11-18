# -*- coding:utf-8 -*-
import Config
import Module.Timer as Timer

from flask import Flask
from flask import render_template, request, jsonify
from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
from Web.CrossdomainAllow import crossdomain
from MySQLExtend.GetPolygon import searchFromAll, searchByIdx
from Jamo import divText



app = Flask(__name__)
searcher = None
Searcher( "new", Config.fromJson("snb.json"))

#url_for("static", filename="style.css")

def retError() :
	return jsonify( result = False )	

@app.route("/")
@app.route("/<title>")
def hello(title = "hello") :
	return render_template('index.html', title=title)

@app.route("/ajax/searchAddress", methods=['POST', 'GET'])
@crossdomain(origin='*')
def ajaxSearchAddress() :

	if request.method == "POST" :
		return retError()

	keyword = request.args.get("keyword", None)

	if keyword is None or keyword == '' :
		return retError()

	result = searchFromAll( "".join( divText( keyword ) ).encode('utf-8') )
	print result

	if isinstance(result, (list, tuple)) and len(result) == 0 :
		return retError()

	return jsonify( result = result )

@app.route("/ajax/searchResult", methods=['POST', 'GET'])
@crossdomain(origin='*')
def ajaxSearchResult() :

	if request.method == "POST" :
		return retError()

	keyword = request.args.get("keyword", None)

	if keyword is None or keyword == '' :
		return retError()


	#result = searcher.
	#print result

	if isinstance(result, (list, tuple)) and len(result) == 0 :
		return retError()

	return jsonify( result = result )


@app.route("/ajax/getPolygon", methods=['POST', 'GET'])
@crossdomain(origin='*')
def ajaxGetPolygon() :

	if request.method == "POST" :
		return retError()

	idx = request.args.get("idx", None)

	if idx is None or idx == '' :
		return retError()

	result = searchByIdx( idx )

	if isinstance(result, (list, tuple)) and len(result) == 0 :
		return retError()

	return jsonify( result = result )


@app.errorhandler(404)
def not_found(error):
    return "404 error..", 404



if __name__== "__main__" :
	app.run(debug=True)