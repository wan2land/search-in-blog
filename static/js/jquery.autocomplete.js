(function($, g) {

	var
	$SearchFormAutocomplete = $( "#SearchFormAutocomplete" );

	g.autocompleteSpatial = function( keyword ) {
		$.ajax({
			type : "GET",
			url : "http://localhost:5000/ajax/searchAddress",
			data : { keyword : keyword },
			success : function( data ) {
				if (data.result == false)
					return
				if (data.result.length == 0)
					return

				var result = "";
				for (var i = 0, len = data.result.length; i < len ; i++) {
					var location = data.result[i];
					result += "<li data-idx=\""+location.idx+"\" data-name=\""+location.name+"\">"+location.name+" ("+location.address+")</li>";
				}

				$SearchFormAutocomplete.find('ul').html(result);
			}

		});
	};


})(jQuery, window);