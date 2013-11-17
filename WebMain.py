# -*- coding:utf-8 -*-
import Module.Timer as Timer

from random import randint
from shapely.geometry import *

from SnbDistrubuteSearcher import Searcher
from Module.RandomText import RandomText
import Config



from flask import Flask
from flask import render_template, request, jsonify
from MySQLExtend.GetPolygon import searchFromAll, searchByIdx
from Jamo import divText

from Web.CrossdomainAllow import crossdomain

app = Flask(__name__)
inst = Searcher( "new", Config.fromJson("parallel.json"), Config.fromJson("mysql.json") )

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