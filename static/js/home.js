;(function($, g){

	var
	map,
	map_center
	;

	var initialize = function() {
		map_center = new google.maps.LatLng(37.544577320855815, 127.02392578125);
		map = new google.maps.Map(document.getElementById('map'), {
			zoom: 13,
			center: map_center,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			disableDoubleClickZoom : true
		});
	};



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

				console.log( g.Geometry.text2geo(data.result) );


				var shape = new GeoJSON( g.Geometry.text2geo( data.result ), {
					strokeColor: "#0000ff",
					strokeOpacity: 0.8,
					strokeWeight: 2,
					fillColor: "#0000ff",
					fillOpacity: 0.35
				});

				console.log( shape );
				shape.setMap(map);

				selectLocationLoading = false;

				return

				if ( recentPolygon !== null ) {
					(function(x) {
						x.setMap(null);
					})(recentPolygon);
				}
				recentPolygon = shape;

				recentPolygon.setMap(map);
				

				return;
				/*
				if (data.result == false)
					return
				if (data.result.length == 0)
					return
				
				var polygon = data.result;
				var newCoords = [];
				var minLatLng = [];
				var maxLatLng = [];
				for (var i in polygon) {
					if (i == 0) {
						minLatLng = [polygon[i][0], polygon[i][1]];
						maxLatLng = [polygon[i][0], polygon[i][1]];
					}
					else {
						if ( minLatLng[0] > polygon[i][0] ) minLatLng[0] = polygon[i][0];
						if ( maxLatLng[0] < polygon[i][0] ) maxLatLng[0] = polygon[i][0];
						if ( minLatLng[1] > polygon[i][1] ) minLatLng[1] = polygon[i][1];
						if ( maxLatLng[1] < polygon[i][1] ) maxLatLng[1] = polygon[i][1];
					}
					newCoords.push( new google.maps.LatLng(polygon[i][0], polygon[i][1]) );
				}
				
				if ( recentPolygon !== null ) {
					(function(x) {
						x.setMap(null);
					})(recentPolygon);
				}
				recentPolygon = new google.maps.Polygon({
					paths: newCoords,
					strokeColor: "#0000ff",
					strokeOpacity: 0.8,
					strokeWeight: 2,
					fillColor: "#0000ff",
					fillOpacity: 0.35
				});

				recentPolygon.setMap(map);
				map.panToBounds( new google.maps.LatLngBounds(
						new google.maps.LatLng(minLatLng[0], minLatLng[1]),
						new google.maps.LatLng(maxLatLng[0], maxLatLng[1])
				));

				selectLocationLoading = false;
				*/
			}

		});
	};


	var formulaRefresh = function() {
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
		selectLocation(formula);
	};
//SearchFormFormula
	$SearchFormAutocomplete.find('ul').on("click", "li", function() {
		var idx = $(this).data('idx');

		$recentSpatialForm.data('idx', idx);
		$recentSpatialForm.val( $(this).data('name') );

		$SearchFormAutocomplete.find('ul').empty();

		formulaRefresh();
	});





	$( '#SearchForm' ).bind("submit", function( e ) {
		e.preventDefault();
		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/searchResult",
			data : 		$(this).serialize(),
			success : function( data ) {
				if (data.result == false)
					return
				if (data.result.length == 0)
					return

				console.log(data.result);
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

	initialize();

})(jQuery, window);