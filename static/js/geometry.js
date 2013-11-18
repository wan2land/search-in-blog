/*!
Made by Seo.day..
*/
/*albnklasdklf */
//aldsnflkasndlfkasd

(function(global){
	"use strict";
	global.Geometry = global.Geometry || {};

	function replaceAll(temp, org, rep){
		return temp.split(org).join(rep)
	}
	global.Geometry.geo2text = function( geo ) {
		// 필요없어.
	};
 	
	//https://github.com/JasonSanford/geojson-google-maps
	global.Geometry.text2geo = function( text ) {
		if(typeof String.prototype.startswith != 'function'){
			String.prototype.startswith = function (str){
				return this.indexOf(str) == 0;
			};
		}
		text = text.toUpperCase();
		var p;
		if(text.startswith("POINT")){
			p = convertPoint(text);
		} else if(text.startswith("LINESTRING")){
			p = convertLinestring(text);
		} else if(text.startswith("POLYGON")){
			p = convertPolygon(text);
		} else if(text.startswith("MULTIPOINT")){
			p = convertMultiPoint(text);
		} else if(text.startswith("MULTILINESTRING")){
			p = convertMultiLineString(text);
		} else if(text.startswith("MULTIPOLYGON")){
			p = convertMultiPolygon(text);
		} else if(text.startswith("GEOMETRYCOLLECTION")){
			p = convertGeometryCollection(text);
		} else {
			alert("No geoType Error");
			return;
		}
		console.log(p);
		return p;
	};

	function convertPoint(text){
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		var pivot = geoString.indexOf(",")
		var lat = geoString.substring(0,pivot)
		var lng = geoString.substring(pivot+1,geoString.length)
		return {
		    "type": "Point",
		    "coordinates": [
		        parseFloat(lat), parseFloat(lng)
		    ]
		};	
	};

	function convertLinestring(text){
		var basket = []
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		geoString = geoString.split(",");
		for(var i = 0; i<geoString.length;i++){
			var smallBasket = []
			var xy = geoString[i].split(" ")
			smallBasket.push(parseFloat(xy[0]),parseFloat(xy[1]))
			basket.push(smallBasket)	
		}
		return {
		    "type": "LineString",
		    "coordinates": 
				basket
		};
	};
	function convertPolygon(text){
		var multiFlag = 0
		if(text.indexOf("m") > -1){
			multiFlag = 1
		}
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		var div = text.indexOf("),(")

		if(div == -1){
			var basket = []
			var exterior = []
			var extString = geoString.substring(1,geoString.length-1)
			extString = extString.split(",")

			for(var i = 0; i<extString.length;i++){
				var tupleXY = []
				var xy = extString[i].split(" ")
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]))
				exterior.push(tupleXY)	
			}
			basket.push(exterior)
		}
		else {
			var basket = []
			var exterior = []
			var interior = []
			geoString = geoString.replace("),(",")|(")
			geoString = geoString.split("|")
			var extString = String(geoString[0])
			extString = extString.substring(1,extString.length-1)
			extString = extString.split(",")

			for(var i = 0; i<extString.length;i++){
				var tupleXY = []
				var xy = extString[i].split(" ")
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]))
				exterior.push(tupleXY)	
			}
			var intString = String(geoString[1])
			intString = intString.substring(1,intString.length-1)
			intString = intString.split(",")
			for(var i = 0; i<intString.length;i++){
				var tupleXY = []
				var xy = intString[i].split(" ")
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]))
				interior.push(tupleXY)	
			}
			basket.push(exterior,interior)
		}
		if(multiFlag == 0){
			return {
			"type": "Polygon",
			"coordinates": 
				basket
			};	
		}
		else {
			return basket
		}
		
	};
	function convertMultiPoint(text){
		var basket = []
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		geoString = geoString.split(",")
		for(var i=0; i<geoString.length; i++){
			var geoString_temp = String(geoString[i])
			geoString_temp = geoString_temp.substring(1,geoString_temp.length-1)
			var tupleXY = []
			var xy = geoString_temp.split(" ")
			tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]))
			basket.push(tupleXY)
		}
		return {
			"type": "MultiPoint",
			"coordinates": 
				basket
		};
	};
	function convertMultiLineString(text){
		var basket = []
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		geoString = replaceAll(geoString,"),(",")|(")
		geoString = geoString.split("|")
		for(var i=0; i<geoString.length; i++){
			var smallBasket= []
			var geoString_temp = String(geoString[i])
			geoString_temp = geoString_temp.substring(1,geoString_temp.length-1)
			geoString_temp = geoString_temp.split(",")
			for(var j=0; j<geoString_temp.length;j++){
				var tupleXY = []
				var xy = geoString_temp[j].split(" ")
				tupleXY.push(parseFloat(xy[0]),parseFloat(xy[1]))	
				smallBasket.push(tupleXY)
			}
			basket.push(smallBasket)
		}
		return {
			"type": "MultiLineString",
			"coordinates": 
				basket
		};
	};
	function convertMultiPolygon(text){
		var basket = []
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		geoString = replaceAll(geoString,")),((","))%((")
		geoString = geoString.split("%")
		for(var i=0;i<geoString.length;i++){
			var geo = convertPolygon("m" + geoString[i])
			basket.push(geo)
		}
		return {
			"type": "MultiPolygon",
			"coordinates": 
				basket
		};
	};
	function convertGeometryCollection(text){
		var basket = []
		var head = text.indexOf("(")
		var geoString = text.substring(head+1,text.length-1)
		geoString = replaceAll(geoString,",POINT","|POINT")
		geoString = replaceAll(geoString,",LINESTRING","|LINESTRING")
		geoString = replaceAll(geoString,",POLYGON","|POLYGON")
		geoString = replaceAll(geoString,",MULTIPOINT","|MULTIPOINT")
		geoString = replaceAll(geoString,",MULTILINESTRING","|MULTILINESTRING")
		geoString = replaceAll(geoString,",MULTIPOLYGON","|MULTIPOLYGON")
		geoString = replaceAll(geoString,",GEOMETRYCOLLECTION","|GEOMETRYCOLLECTION")
		geoString = geoString.split("|")
		for(var i=0;i<geoString.length;i++){
			basket.push(Geometry.text2geo(geoString[i]))
		}
		return {
			"type": "GeometryCollection",
			"coordinates": 
				basket
		};
	};
/*
	global.Geometry.checkerFormat = function (){
		console.log ( {
			"type": "Point",
    		"coordinates": [
        		-80.66252,
        		35.04267
    		]
		});

		console.log( {
			"type": "LineString",
   			"coordinates": [
        		[-80.661983228058659, 35.042968081213758],
        		[-80.662076494242413, 35.042749414542243],
        		[-80.662196794397431, 35.042626481357232],
        		[-80.664238981504525, 35.041175532632963]
    		]
		});

		console.log( {
   			"type": "Polygon",
            "coordinates": [
            	[
                    [-80.662120612605904, 35.042875219905184],
                    [-80.662141716053014, 35.042832740965068],
                    [-80.662171938563816, 35.042789546962993],
                    [-80.662209174653029, 35.042750233165179],
                    [-80.662250709107454, 35.042716920859959],
                    [-80.664191013603950, 35.041343401901145],
                    [-80.664311100312809, 35.041354401320908],
                    [-80.664601012011108, 35.041627401070109],
                    [-80.662899986829899, 35.042822078075667],
                    [-80.662638586829899, 35.043032078075667],
                    [-80.662595574310288, 35.043162322407341],
                    [-80.662142312824884, 35.043015448098977],
                    [-80.662145396323511, 35.042970839922489],
                    [-80.662117972448982, 35.042908385949438],
                    [-80.662120612605904, 35.042875219905184]
                ],
                [
                    [-80.663660240030611, 35.042285014551399],
                    [-80.663323010340658, 35.041963021011493],
                    [-80.663477030360489, 35.041855013227392],
                    [-80.663801010040396, 35.042180031153971]
                ]
            ]
		})
		
		console.log( {
			"type": "MultiPoint",
            "coordinates": [
                [-80.66252, 35.04267],
                [-80.66240, 35.04255]
            ]
		})

		console.log({
			"type": "MultiLineString",
                        "coordinates": [
                                [
                                        [-80.661983228058659, 35.042968081213758],
                                        [-80.662076494242413, 35.042749414542243],
                                        [-80.662196794397431, 35.042626481357232],
                                        [-80.664238981504525, 35.041175532632963]
                                ],[
                                        [-80.660716952851203, 35.043580586227073],
                                        [-80.660819057590672, 35.042614204165666],
                                        [-80.660860211132032, 35.042441083434795],
                                        [-80.660927975876391, 35.042312940446855],
                                        [-80.661024889425761, 35.042200170467524],
                                        [-80.661384194084519, 35.041936069070361]
                                ]
                        ]
		})
		
		console.log({
			"type": "MultiPolygon",
                        "coordinates": [
                                [
                                        [
                                                [-80.661917125299155, 35.042245264120233],
                                                [-80.662257428469147, 35.042566288770765],
                                                [-80.662116500253873, 35.042670715828088],
                                                [-80.661715367137106, 35.042389935257198],
                                                [-80.661917125299155, 35.042245264120233]
                                        ]
                                ],[
                                        [
                                                [-80.661547137566686, 35.042510563404129],
                                                [-80.661677171806787, 35.042417322902836],
                                                [-80.662084018102888, 35.042702102858307],
                                                [-80.662039854197829, 35.042756211162953],
                                                [-80.662002555672572, 35.042820528162387],
                                                [-80.661457640151127, 35.042647387136952],
                                                [-80.661547137566686, 35.042510563404129]
                                        ]
                                ]
                        ]


		})
		console.log({
			"type": "GeometryCollection",
                        "geometries": [
                                {
                                        "type": "Point",
                                        "coordinates": [-80.66256, 35.04271]
                                },{
                                        "type": "MultiPolygon",
                                        "coordinates": [
                                                [
                                                        [
                                                                [-80.661917125299155, 35.042245264120233],
                                                                [-80.662257428469147, 35.042566288770765],
                                                                [-80.662116500253873, 35.042670715828088],
                                                                [-80.661715367137106, 35.042389935257198],
                                                                [-80.661917125299155, 35.042245264120233]
                                                        ]
                                                ],[
                                                        [
                                                                [-80.661547137566686, 35.042510563404129],
                                                                [-80.661677171806787, 35.042417322902836],
                                                                [-80.662084018102888, 35.042702102858307],
                                                                [-80.662039854197829, 35.042756211162953],
                                                                [-80.662002555672572, 35.042820528162387],
                                                                [-80.661457640151127, 35.042647387136952],
                                                                [-80.661547137566686, 35.042510563404129]
                                                        ]
                                                ]
                                        ]
                                },{
                                        "type": "LineString",
                                        "coordinates": [
                                                [-80.661983228058659, 35.042968081213758],
                                                [-80.662076494242413, 35.042749414542243],
                                                [-80.662196794397431, 35.042626481357232],
                                                [-80.664238981504525, 35.041175532632963]
                                        ]
                                }
                        ]
		})
	};
*/	
})(window);