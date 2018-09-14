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

	$('.view_filter').on('click', function(e){
		data['type_view'] = $(this).data('view-filter');
		// console.log(data['type_view'])
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});

	$('.type_currency').on('click', function(e){
		data['type_currency'] = $(this).data('currency');
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});

	$('#reset').on('click', function(e){
		// e.PreventDefault();
		data['reset'] = true;
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		SendAjax();
	});
    
    function SendAjax(){
		$.ajax({
			url: 'http://127.0.0.1:8000/filter/',
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