( function( $ ) {

	$( window ).load( function() {

		// If Infinite Scroll is active.
		if ( $( 'body' ).hasClass( 'infinite-scroll' ) ) {
			$( '.archive .hentry, .blog .hentry, .search-results .hentry' ).each( function() {
				$( this ).addClass( 'post-loaded' )
				         .fadeTo( 125, 1 );
			} );
			if ( $( '#infinite-handle' ).length > 0 ) {
				$( 'body' ).addClass( 'infinity-handle' );
			}

			// Layout posts that arrive via infinite scroll.
			$( document.body ).on( 'post-load', function () {

				// Completly remove .infinite-loader
				$( '.infinite-loader' ).each( function() {
					if ( ! $( this ).is( ':visible' )  ) {
						$( this ).remove();
					}
				} );

				// Force layout correction after 125 milliseconds.
				setTimeout( function() {
					$( '#infinite-handle' ).show();
					if ( $( '#infinite-handle' ).length === 0 && $( 'body' ).hasClass( 'infinity-handle' ) ) {
						$( 'body' ).addClass( 'infinity-end' );
					}
					var delay = 0;
					$( '.hentry:not(.post-loaded)' ).each( function() {
						$( this ).addClass( 'post-loaded' )
						         .delay( delay++ * 125 ).fadeTo( 125, 1 );
					} );
				}, 125 );
			} );
		}

	} );

} )( jQuery );
