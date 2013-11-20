google.maps.Polygon.prototype.my_getBounds=function(){
    var bounds = new google.maps.LatLngBounds()
    this.getPath().forEach(function(element,index){bounds.extend(element)})
    return bounds
}

;(function($, g){

	var
	map,
	map_center
	;

	map_center = new google.maps.LatLng(37.544577320855815, 127.02392578125);
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 13,
		center: map_center,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		disableDoubleClickZoom : true
	});

	var make_polygon_point = [];
	var make_polygon_coords = [];
	var make_polygon = null;
	google.maps.event.addListener(map, "dblclick", function( e ) {
		if ( make_polygon !== null ) {
			make_polygon.setMap(null);
		}
		make_polygon_point.push( [e.latLng.lat(), e.latLng.lng()] );
		make_polygon_coords.push( e.latLng );

		if (make_polygon_point.length > 2) {
			make_polygon = new google.maps.Polygon({
				paths : make_polygon_coords,
				map : map
			});
			google.maps.event.addListener(make_polygon, "click", function( e ) {
				var result = []; //"POLYGON((";
				for (var i = 0; i < make_polygon_point.length; i++) {
					result.push( make_polygon_point[i][0] + " " + make_polygon_point[i][1] );
				}
				result.push( make_polygon_point[0][0] + " " + make_polygon_point[0][1] )
				alert( "POLYGON((" + result.join(",") + "))" );
				make_polygon_point = [];
				make_polygon_coords = [];
				make_polygon.setMap(null);
			});

		}
	});

	var $SearchFormSpatial = $("#SearchFormSpatial");
	var $SearchFormFormula = $( "#SearchFormFormula");
	var $SearchFormAutocomplete = $( "#SearchFormAutocomplete" );

	var $recentSpatialForm = null;

	//Location Polygon Loading!!
	var selectLocationLoading = false;
	var recentPolygon = null;
	var selectLocation = function( formula ) {

		if (selectLocationLoading) return;
		selectLocationLoading = true;

		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/getPolygon",
			data : { formula : formula },
			success : function( data ) {

				// clear map
				if ( recentPolygon !== null ) {
					if (recentPolygon.length) {
						for (var i = 0, len = recentPolygon.length; i < len; i++) {
							if (recentPolygon[i].length) {
								for (var j = 0, jlen = recentPolygon[i].length; j < jlen; j++) {
									recentPolygon[i][j].setMap(null);
								}
							}
							else {
								recentPolygon[i].setMap(null);
							}
						}
					}
					else {
						recentPolygon.setMap(null);
					}
				}

				recentPolygon = new GeoJSON( g.Geometry.text2geo( data.result ) );

				if (recentPolygon.type && recentPolygon.type == "Error"){
					return;
				}
				if (recentPolygon.length) {
					for (var i = 0; i < recentPolygon.length; i++) {
						if(recentPolygon[i].length) {
							for(var j = 0; j < recentPolygon[i].length; j++){
								recentPolygon[i][j].setMap(map);
							}
						}
						else{
							recentPolygon[i].setMap(map);
						}
					}
				}
				else{
					recentPolygon.setMap(map)
				}

				selectLocationLoading = false;

			}

		});
	};
	var getFormula = function() {
		var spatial_groups = $SearchFormSpatial.find('div.group');
		var formula = "";

		for (var i = 0, len = spatial_groups.length; i < len; i++) {
			var spatial_group = spatial_groups.eq(i);

			var spatial_loc = spatial_group.find('input.spatial-name').data('idx');
			var spatial_operator = spatial_group.find('select.spatial-operator').find('option:selected').val();

			formula += spatial_loc;
			formula += spatial_operator;

			if (spatial_operator === "=") break;
		}
		return formula;
	};

	var formulaRefresh = function() {
		selectLocation( getFormula() );
	};
//SearchFormFormula
	$SearchFormAutocomplete.find('ul').on("click", "li", function() {
		var idx = $(this).data('idx');

		$recentSpatialForm.data('idx', idx);
		$recentSpatialForm.val( $(this).data('name') );

		$SearchFormAutocomplete.find('ul').empty();

		formulaRefresh();
	});



	var recentResults = [];

	$( '#SearchForm' ).bind("submit", function( e ) {
		e.preventDefault();
		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/searchResult",
			data : {
				"operator" : $('#SearchFormOperate').find('option:selected').val(),
				"formula" : getFormula(),
				"keyword" : $("#SearchFormKeyword").val()
			},
			success : function( data ) {
				if ( data.result === false ) return;
				if ( data.result.length ) {

					// clear Marker!!
					if (recentResults.length) {
						for (var i = 0, len = recentResults.length; i < len; i++) {
							recentResults[i].setMap(null);
						}
					}

					for (var i = 0, len = data.result.length; i < len ; i++) {
						var get_geo = g.Geometry.text2geo( data.result[i][0] );
						if (get_geo.type === "Point") {
							var latlng = get_geo.coordinates;

							recentResults[i] = new google.maps.Marker({
								position : new google.maps.LatLng( latlng[1], latlng[0] ),
								animation: google.maps.Animation.DROP,
								map : map
							});
							(function(marker, title, url){
								var infowindow = new google.maps.InfoWindow({
									content: '<div class="title">' + title + '</div>'
								});
								google.maps.event.addListener(recentResults[i], 'mouseover', function() {
									infowindow.open(map, marker);
								});
								google.maps.event.addListener(recentResults[i], 'mouseout', function() {
									infowindow.close();
								});
								google.maps.event.addListener(recentResults[i], 'click', function() {
									window.open(url);
								});


							})(recentResults[i], data.result[i][1], data.result[i][2]);
						}
						else if (get_geo.type === "Polygon") {
							var points = get_geo.coordinates[0];
							var coords = [];
							for (var j = 0, jlen = points.length; j < jlen; j++) {
								coords.push( new google.maps.LatLng( points[j][1], points[j][0] ));
							}

							recentResults[i] = new google.maps.Polygon({
								paths : coords,
								strokeColor: '#57a1f3',
								strokeOpacity: 0.8,
								strokeWeight: 3,
								fillColor: '#90bef3',
								fillOpacity: 0.35,
								map : map
							});

							(function(marker, title, url){
								var infowindow = new google.maps.InfoWindow({
									content: '<div class="title">' + title + '</div>'
								});
								var is_hover = false;
								google.maps.event.addListener(recentResults[i], 'mouseover', function( e ) {
									if (is_hover) return;
									is_hover = true;
									infowindow.open(map);
									infowindow.setPosition( e.latLng );
								});
								google.maps.event.addListener(recentResults[i], 'mouseout', function() {
									infowindow.close();
									is_hover = false;
								});
								google.maps.event.addListener(recentResults[i], 'click', function() {
									window.open(url);
								});


							})(recentResults[i], data.result[i][1], data.result[i][2]);

						}
						//recentMark
						//(new google.maps.InfoWindow({

						//})).open(map,marker);
					}

				}
			},
			error : function( data ) {
				console.log( "error");
				// ^^;
			}

		});		
	});

	$SearchFormSpatial.on("keyup", "input", function() {
		$recentSpatialForm = $(this);
		var keyword = $(this).val();
		$SearchFormAutocomplete.css("left", $(this).offset().left );
		g.autocompleteSpatial( keyword );
	});

	var spatial_append_context = $SearchFormSpatial.html();
	$SearchFormSpatial.on("change", "select", function() {
		
		var $group = $(this).parent();

		formulaRefresh();

		// 오퍼레이터가 = 이면.
		if ( $(this).find('option:selected').val() === "=" ) {
			$group.nextAll().addClass('hidden');
			return;
		}

		// 나머지 오퍼레이터일때.
		// 다음에 뭔가 있으면 
		if ( $group.next().length !== 0 ) {
			var $next = $group.next();
			while ( true ) {
				$next.removeClass('hidden');
				if ( $next.find('select.spatial-operator').find('option:selected').val() === "=" ) {
					break;
				}
				$next = $next.next();
			}
			return;
		}

		$SearchFormSpatial.append( spatial_append_context );
	});


})(jQuery, window);