$(document).ready(function(){
	// Forming csrf_token
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie != '') {
			let cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				let cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	};

	let data = {};

	//Ico Open/Close window
	$('.filter-ico').on('click', function(){
		$('.filter-window').toggle();
	})

	//Button Close
	$('.close-button-filter').on('click', function(){
		$('.filter-window').toggle();
	})

	// filter by
	$('.type_filter').on('click', function(e){
		data['type_filter'] = $(this).data('book-f');
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});
	
	function SendAjax(){
		$.ajax({
			url: 'https://bookworm-altheone.herokuapp.com/filter/',
			method: 'POST',
			data: data,
			cached: true,
			success: function(data){
				setTimeout(function() {window.location.reload();}, 500)
			},
			error: function(e){
				console.log(e);
			}
		})
	}
})