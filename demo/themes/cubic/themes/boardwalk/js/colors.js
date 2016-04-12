( function( $ ) {

	function boardwalk_colors() {
		var unique_randoms = [];
		var num_randoms = 5;
		function make_unique_random() {

			// refill the array if needed
		    if ( ! unique_randoms.length ) {
		        for ( var i = 0; i < num_randoms; i++ ) {
		            unique_randoms.push( i );
		        }
		    }
		    var index = Math.floor( Math.random() * unique_randoms.length );
		    var val = unique_randoms[index];

		    // now remove that value from the array
		    unique_randoms.splice( index, 1 );

		    return val;

		}

		$( '.hentry' ).each( function() {
			if ( ! $( this ).hasClass( 'color-done' ) ) {
				$( this ).addClass( 'color-done color-' + ( make_unique_random() + 1 ) );
			}
		} );
	}

	$( window ).load( boardwalk_colors );

	$( document ).on( 'post-load', boardwalk_colors );

} )( jQuery );
