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

	$('.add-author').on('click', function(e){
		e.preventDefault();
		data['first_name'] = $('#id_first_name').val();
		data['secondary_name'] = $('#id_secondary_name').val();
		data['last_name'] = $('#id_last_name').val();
		SendAjax('author');
	})

	$('.add-attributes').on('click', function(e){
		e.preventDefault();
		data['name'] = $('#id_name').val();
		data['value'] = $('#id_value').val();
		SendAjax('attributes');
	})

	$('.add-genre').on('click', function(e){
		e.preventDefault();
		data['title'] = $('.input_genre_title').val();
		data['slug'] = $('.input_genre_slug').val();
		SendAjax('genre');
	})

	$('.add-tags').on('click', function(e){
		e.preventDefault();
		data['title'] = $('.input_tags_title').val();
		data['slug'] = $('.input_tags_slug').val();
		SendAjax('tags');
	})

	$('.add-phouse').on('click', function(e){
		e.preventDefault();
		data['title'] = $('.input_phouse_title').val();
		SendAjax('phouse');
	})


	function SendAjax(action){
		data['csrfmiddlewaretoken'] = getCookie('csrftoken');
		$.ajax({
			url: 'http://127.0.0.1:8000/add-' + action + '/',
			method: 'POST',
			data: data,
			cached: true,
			success: function(data){
				console.log(data);
				if(data['status'] == true){
					console.log('Okk!');
					$('#id_'+ action +'').append('<option value="'+ data['id'] +'" selected>'+ data['title'] +'</option>');
					$('.close-button-'+action).trigger('click');
					$('.form_'+action)[0].reset();
				}
				if(data['status'] == false){
					console.log('Bad...!');
				}
			},
			error: function(e){
				console.log(e);
			}
		})
	}

})