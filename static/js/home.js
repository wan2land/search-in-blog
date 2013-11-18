;(function($){

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

		/*
		google.maps.event.addListener(map, "dblclick", function ( e ){
			console.log( e.latLng.lat(), e.latLng.lng() );
		});
		google.maps.event.addListener(map, "zoom_changed", function(){
			//console.log(map.getZoom());
			// 7~10 -> 서울시 부산시, 시단위로..
			// 11~13 -> 구단위
			// 14~ -> 동단위..
		});
		google.maps.event.addListener(map, "mousemove", function( e ) {
			//console.log( e.latLng.lat(), e.latLng.lng() );
		});
		*/
	};



	var
	$SearchFormAutocomplete = $( "#SearchFormAutocomplete" )
	;
	var autocompleteSpatial = function( keyword ) {
		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/searchAddress",
			data : { keyword : keyword },
			success : function( data ) {
				if (data.result == false)
					return
				if (data.result.length == 0)
					return

				var result;
				for (var i = 0, len = data.result.length; i < len ; i++) {
					var location = data.result[i];
					result += "<li data-idx=\""+location.idx+"\">"+location.name+" ("+location.address+")</li>";
				}

				$SearchFormAutocomplete.find('ul').html(result);

			}

		});
	};



	var selectLocationLoading = false;
	var recentPolygon = null;
	var selectLocation = function(idx) {
		if (selectLocationLoading) return;
		selectLocationLoading = true;

		$( '[name=multi_spatial]' ).val(idx);

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
	$SearchFormAutocomplete.find('ul').on("click", "li", function() {
		selectLocation( $(this).data('idx') );
	});





	$( '#SearchForm' ).bind("submit", function( e ) {
		e.preventDefault();

		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/searchResult",
			data : { keyword : 'a' },
			success : function( data ) {
				if (data.result == false)
					return
				if (data.result.length == 0)
					return

				var result;
				for (var i = 0, len = data.result.length; i < len ; i++) {
					var location = data.result[i];
					result += "<li data-idx=\""+location.idx+"\">"+location.name+" ("+location.address+")</li>";
				}

				$SearchFormAutocomplete.find('ul').html(result);

			}

		});		
	});
	$( '#SearchFormSpatial' ).bind("keyup", function() {
		autocompleteSpatial( $(this).val() );
	});

	initialize();

})(jQuery);