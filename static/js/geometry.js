/*!
Made by Seo.daehyun
*/
(function(global){
	"use strict";
	global.Geometry = global.Geometry || {};

	function replaceAll(temp, org, rep){
		return temp.split(org).join(rep);
	}

	//https://github.com/JasonSanford/geojson-google-maps
	global.Geometry.text2geo = function( text ) {
		
		if(typeof String.prototype.startswith != 'function'){
			String.prototype.startswith = function (str){
				return this.indexOf(str) == 0;
			};
		}

		var geo;
		text = text.toUpperCase();
		
		if(text.startswith("POINT")){
			geo = convertPoint(text);
		} else if(text.startswith("LINESTRING")){
			geo = convertLinestring(text);
		} else if(text.startswith("POLYGON")){
			geo = convertPolygon(text);
		} else if(text.startswith("MULTIPOINT")){
			geo = convertMultiPoint(text);
		} else if(text.startswith("MULTILINESTRING")){
			geo = convertMultiLineString(text);
		} else if(text.startswith("MULTIPOLYGON")){
			geo = convertMultiPolygon(text);
		} else if(text.startswith("GEOMETRYCOLLECTION")){
			geo = convertGeometryCollection(text);
		} else {
			alert("It is NOT GeometryType");
			return;
		}
		console.log(geo);
		return geo;
	};

	function convertPoint(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		var pivot = geoString.indexOf(",");
		var lat = geoString.substring(0,pivot);
		var lng = geoString.substring(pivot+1,geoString.length);
		basket.push(parseFloat(lat),parseFloat(lng));
		return {
			"type": "Point",
			"coordinates": basket
		};	
	};

	function convertLinestring(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		geoString = geoString.split(",");
		for(var i = 0; i<geoString.length;i++){
			var smallBasket = [];
			var xy = geoString[i].split(" ");
			smallBasket.push(parseFloat(xy[0]),parseFloat(xy[1]));
			basket.push(smallBasket);
		}
		return {
			"type": "LineString",
			"coordinates": basket
		};
	};

	function convertPolygon(text){
		var multiFlag = 0;
		if(text.indexOf("m") > -1){
			multiFlag = 1;
		}
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		var div = text.indexOf("),(");

		if(div == -1){
			var basket = [];
			var exterior = [];
			var extString = geoString.substring(1,geoString.length-1);
			extString = extString.split(",");

			for(var i = 0; i<extString.length;i++){
				var tupleXY = [];
				var xy = extString[i].split(" ");
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]));
				exterior.push(tupleXY);
			}
			basket.push(exterior);
		}
		else {
			var basket = [];
			var exterior = [];
			var interior = [];
			geoString = geoString.replace("),(",")|(");
			geoString = geoString.split("|");
			var extString = String(geoString[0]);
			extString = extString.substring(1,extString.length-1);
			extString = extString.split(",");

			for(var i = 0; i<extString.length;i++){
				var tupleXY = [];
				var xy = extString[i].split(" ");
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]));
				exterior.push(tupleXY);
			}
			var intString = String(geoString[1]);
			intString = intString.substring(1,intString.length-1);
			intString = intString.split(",");
			for(var i = 0; i<intString.length;i++){
				var tupleXY = [];
				var xy = intString[i].split(" ");
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]));
				interior.push(tupleXY);
			}
			basket.push(exterior,interior);
		}
		if(multiFlag == 0){
			return {
			"type": "Polygon",
			"coordinates": basket
			};	
		} else {
			return basket;
		}
	};

	function convertMultiPoint(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		geoString = geoString.split(",");
		for(var i=0; i<geoString.length; i++){
			var geoString_temp = String(geoString[i]);
			geoString_temp = geoString_temp.substring(1,geoString_temp.length-1);
			var tupleXY = [];
			var xy = geoString_temp.split(" ");
			tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]));
			basket.push(tupleXY);
		}
		return {
			"type": "MultiPoint",
			"coordinates": basket
		};
	};

	function convertMultiLineString(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		geoString = replaceAll(geoString,"),(",")|(");
		geoString = geoString.split("|");
		for(var i=0; i<geoString.length; i++){
			var smallBasket= [];
			var geoString_temp = String(geoString[i]);
			geoString_temp = geoString_temp.substring(1,geoString_temp.length-1);
			geoString_temp = geoString_temp.split(",");
			for(var j=0; j<geoString_temp.length;j++){
				var tupleXY = [];
				var xy = geoString_temp[j].split(" ");
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]));
				smallBasket.push(tupleXY);
			}
			basket.push(smallBasket);
		}
		return {
			"type": "MultiLineString",
			"coordinates": basket
		};
	};

	function convertMultiPolygon(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		geoString = replaceAll(geoString,")),((","))%((");
		geoString = geoString.split("%");
		for(var i=0;i<geoString.length;i++){
			var geo = convertPolygon("m" + geoString[i]);
			basket.push(geo);
		}
		return {
			"type": "MultiPolygon",
			"coordinates": basket
		};
	};

	function convertGeometryCollection(text){
		var basket = [];
		var head = text.indexOf("(");
		var geoString = text.substring(head+1,text.length-1);
		geoString = replaceAll(geoString,",POINT","|POINT");
		geoString = replaceAll(geoString,",LINESTRING","|LINESTRING");
		geoString = replaceAll(geoString,",POLYGON","|POLYGON");
		geoString = replaceAll(geoString,",MULTIPOINT","|MULTIPOINT");
		geoString = replaceAll(geoString,",MULTILINESTRING","|MULTILINESTRING");
		geoString = replaceAll(geoString,",MULTIPOLYGON","|MULTIPOLYGON");
		geoString = replaceAll(geoString,",GEOMETRYCOLLECTION","|GEOMETRYCOLLECTION");
		geoString = geoString.split("|");
		for(var i=0;i<geoString.length;i++){
			basket.push(Geometry.text2geo(geoString[i]));
		}
		return {
			"type": "GeometryCollection",
			"geometries": basket
		};
	};

})(window);