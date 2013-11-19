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



	var $SearchFormSpatial = $("#SearchFormSpatial");
	var $SearchFormFormula = $( "#SearchFormFormula");
	var $SearchFormAutocomplete = $( "#SearchFormAutocomplete" );

	var $recentSpatialForm = null;

	//Location Polygon Loading!!
	var selectLocationLoading = false;
	var recentPolygon = null;
	var selectLocation = function( formula ) {

		console.log(formula);
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

				g.mapp = map;
				g.foo = recentPolygon = new GeoJSON( g.Geometry.text2geo( data.result ) );

				console.log( g.Geometry.text2geo( data.result ));

				if (recentPolygon.type && recentPolygon.type == "Error"){
					return;
				}
				if (recentPolygon.length) {
					for (var i = 0; i < recentPolygon.length; i++) {
						if(recentPolygon[i].length) {
							for(var j = 0; j < recentPolygon[i].length; j++){
								recentPolygon[i][j].setMap(map);
								if(recentPolygon[i][j].geojsonProperties) {
									setInfoWindow(recentPolygon[i][j]);
								}
							}
						}
						else{
							recentPolygon[i].setMap(map);
						}
						if (recentPolygon[i].geojsonProperties) {
							setInfoWindow(recentPolygon[i]);
						}
					}
				}
				else{
					recentPolygon.setMap(map)
					if (recentPolygon.geojsonProperties) {
						setInfoWindow(recentPolygon);
					}
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


})(jQuery, window);