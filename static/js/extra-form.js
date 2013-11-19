(function($){

	var $placeholder = $( '[data-placeholder]' );

	$placeholder.bind("focus", function() {
		var o = $(this);
		if ( o.text() === o.data('placeholder') ) {
			o.text('').css('color', '#000');
		}
	}).bind("blur", function() {
		var o = $(this);
		if ( o.text() === '' || o.text() === o.data('placeholder') ) {
			o.text( o.data('placeholder') ).css('color', '#a9a9a9');
		}
	}).each(function() {
		if ( $(this).text() === '' ) {
			$(this).text( $(this).data('placeholder') ).css('color', '#a9a9a9');
		}
	});


})(jQuery);