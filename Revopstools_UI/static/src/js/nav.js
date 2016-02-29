$(document).ready(function() {

	var stickyNavTop = $("nav").offset().top;

	var stickyNav = function() {
	var scrollTop = $(window).scrollTop();

	if (scrollTop > stickyNavTop) {
		$(nav).addClass('sticky');
	} else {
		$(nav).removeClass('sticky');
	}
	};

	stickyNav();

	$(window).scroll(function() {
		stickyNav();
	});
});

$(document).ready(function() {
	$('.valueCPM_button').click(function() {
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