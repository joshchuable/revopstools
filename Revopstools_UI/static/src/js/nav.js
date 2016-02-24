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

$(function() {
	$('valueCPM_button').click(function() {
		$.ajax({
			url: '/pyscripts/valueCPM_calc',
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(erorr);
			}
		});
	});
});