// -----------------------
//	DOCUMENT READY
// ----------------------


$(document).ready(function() {
	alert("Doc is ready");
	$('.ref-link').on('click',function (event) {
		// body...
		event.preventDefault();

		alert('you clicked');

		//Make description and overlay visible
		$('.js-des-overlay').addClass('is-visible');
		$(this).next('div').addClass('is-visible');

		//Make description and overlay invisible
		$('.js-des-overlay').on('click',function(event) {
			$(this).removeClass('is-visible');
			$('.des').removeClass('is-visible');
		});


	});
});




/*$('.topic-ref-des-link').on('click',function(event) {
		event.preventDefault();

		$('this').parent().find('.topic-ref-des').addClass('is-visible');
		$('.js-des-overlay').addClass('is-visible');

		$('.js-close').on('click',function (event) {
			$('this').parent().parent().removeClass('is-visible');
			$('.js-des-overlay').removeClass('is-visible');
		})
	});	*/