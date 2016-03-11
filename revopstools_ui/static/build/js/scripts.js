$(document).ready(function() {
	$('#progress-bar').progressbar({
		value: false
	});
	$('.button-progress').click(function() {
		$('.notification-container').toggleClass('hidden');
		$('#progress-bar').progressbar( "enable" );
	});
});
$(document).ready(function() {
	$('#nav').css('min-height', $(window).height()+'px');
	$(window).resize(function() {
		$('#nav').css('min-height', $(window).height()+'px');
	});
});
$(document).ready(function() {
	$('#valueCPM_button').click(function() {
		$.ajax({
			url: '/pyscripts/valueCPM_calc',
			type: 'GET',
			success: function(response) {
				console.log("File download will begin momentarily...");
				var url = '/pyscripts/valueCPM_calc?data=' + response;
				window.location = url;
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});