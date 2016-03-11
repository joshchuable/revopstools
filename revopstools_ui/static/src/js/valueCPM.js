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