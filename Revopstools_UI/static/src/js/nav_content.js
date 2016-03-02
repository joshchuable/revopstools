// $(document).ready(function() {

// 	var stickyNavTop = $("nav").offset().top;

// 	var stickyNav = function() {
// 	var scrollTop = $(window).scrollTop();

// 	if (scrollTop > stickyNavTop) {
// 		$(nav).addClass('sticky');
// 	} else {
// 		$(nav).removeClass('sticky');
// 	}
// 	};

// 	stickyNav();

// 	$(window).scroll(function() {
// 		stickyNav();
// 	});
// });

$(document).ready(function() {
	$('#nav').css('min-height', $(window).height()+'px');
	$(window).resize(function() {
		$('#nav').css('min-height', $(window).height()+'px');
	});
	$('#content').css('width', ($(window).width()-$('#nav').width())+'px');
	$(window).resize(function() {
		$('#content').css('width', ($(window).width()-$('#nav').width())+'px');
	});
});