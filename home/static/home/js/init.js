$( 'document' ).ready(function() {
	/* to protect against unloaded script */
	function load(src, callback) {
		var script = document.createElement('script');
		script.setAttribute('type', "text/javascript");
		script.setAttribute('src', src);
		var loaded = false;
		if(callback) {
			script.onload = function() {
				if(!loaded) {
					callback();
				}
				loaded = true;
			};
		}
		document.getElementsByTagName('head')[0].appendChild(script);
	}
	
	function initialize() {
		$( '.bxSlider' ).bxSlider({
			slideWidth: 960
		});
	}
	
	load('static/home/js/html5lightbox/html5lightbox.js');
	load('static/home/js/bxslider/jquery.bxslider.min.js', initialize);
});