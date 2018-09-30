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
	
	$('#user-ico').on('click', function(){
		$('.user-window').toggle();
	})
	$('.close-button-user').on('click', function(){
		$('.user-window').toggle();
	})

	$('#feedback-ico').on('click', function(){
		$('.feedback-window').toggle();
	})
	$('.close-button-feedback').on('click', function(){
		$('.feedback-window').toggle();
	})

	$('#setting-ico').on('click', function(){
		$('.setting-window').toggle();
	})
	$('.close-button-setting').on('click', function(){
		$('.setting-window').toggle();
	})

	let data = {}

	$('.view_filter').on('click', function(){
		data['type_view'] = $(this).data('view-filter');
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});

	$('#currency-selector').change(function(){
		data['type_currency'] = $(this).children(":selected").data('currency');
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});

	$('#reset').on('click', function(){
		data['reset'] = true;
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});

	$('.guest-comment').on('click', function(){
		$('.regist-button').trigger('click');
	})
	
	function SendAjax(){
		$.ajax({
			url: 'https://bookworm-altheone.herokuapp.com/filter/',
			method: 'POST',
			data: data,
			cached: true,
			success: function(data){
				console.log('Okk!');
				setTimeout(function() {window.location.reload();}, 500)
			},
			error: function(e){
				console.log(e);
			}
		})
	}

})