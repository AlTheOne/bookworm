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

	$('input[name=books]').on('click', function(){
		if($('#form_cart input:checkbox:checked').length > 0){
			console.log('Есть выбранные');
			$('button[value=buy-all]').hide();
			$('button[value=buy-selected]').show();
		}else{
			$('button[value=buy-all]').show();
			$('button[value=buy-selected]').hide();
			console.log('Нет выбранных');
		}
	})

	$('.book-price-div').on('click', function(e){
		e.preventDefault();
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		data['incart'] = $(this).data('id');
		SendAjax();
	})

	function SendAjax(){
		$.ajax({
			url: 'bookworm-altheone.herokuapp.com/mycart/add/',
			method: 'POST',
			data: data,
			cached: true,
			success: function(data){
				if(data['status'] == '200'){
					$('.cart-count').text(parseInt($('.cart-count').text()) + 1);
				}
			},
			error: function(e){
				console.log(e);
			}
		})
	}

})