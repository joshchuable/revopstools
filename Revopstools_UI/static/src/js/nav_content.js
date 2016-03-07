$(document).ready(function() {
	$('#nav').css('min-height', $(window).height()+'px');
	$(window).resize(function() {
		$('#nav').css('min-height', $(window).height()+'px');
	});
});