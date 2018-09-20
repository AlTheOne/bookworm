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
	
	function totalPrice(){
		let tp_cart = 0;
		$('.price').each(function(){
			tp_cart = tp_cart + parseFloat($(this).text());
		})
		$('#total_order_amount').text(tp_cart.toFixed(2));
	}
	totalPrice();

	$('.outcart').on('click', function(e){
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		data['outcart'] = $(this).data('id');
		SendAjax('del', data['outcart']);
	})

	function SendAjax(action, someid){
		$.ajax({
			url: 'http://127.0.0.1:8000/mycart/' + action + '/',
			method: 'POST',
			data: data,
			cached: true,
			success: function(data){
				if(data['status'] == '200'){
					console.log('Okk!');
					$('.object'+someid).remove();
					$('.cart-count').text( parseInt($('.cart-count').text()) - 1);
					totalPrice();
				}
			},
			error: function(e){
				console.log(e);
			}
		})
	}

})