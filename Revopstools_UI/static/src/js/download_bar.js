$(document).ready(function() {
	$('#progress-bar').progressbar({
		value: false
	});
	$('.button-progress').click(function() {
		$('.notification-container').toggleClass('hidden');
		$('#progress-bar').progressbar( "enable" );
	});
});