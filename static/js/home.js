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
	var selectLocation = function(idx) {
		if (selectLocationLoading) return;
		selectLocationLoading = true;

		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/getPolygon",
			data : { idx : idx },
			success : function( data ) {
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
			}

		});
	};


	var formulaRefresh = function() {
		console.log( $SearchFormSpatial.find('input.spatial-name') );
	};
//SearchFormFormula
	$SearchFormAutocomplete.find('ul').on("click", "li", function() {
		var idx = $(this).data('idx');

		$recentSpatialForm.data('idx', idx);
		$recentSpatialForm.val( $(this).data('name') );

		$SearchFormAutocomplete.find('ul').empty();

		formulaRefresh();

		selectLocation( idx );
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
		if ( $(this).find('option:selected').val() === "none" ) return;
		$SearchFormSpatial.append( $SearchFormSpatial.html() );
	});

	initialize();

})(jQuery, window);