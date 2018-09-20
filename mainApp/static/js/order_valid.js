$(document).ready(function(){

	// Зона функций
	function test_error(data){
		let variable = $(this).val();
		let reg = new RegExp($(this).attr('pattern'));

		if(reg.test(variable) === false){
			console.log(data.data.text);
			$(this).css('border-color', '#FF0000');
			return false;
		}

		$(this).css('border-color', '#00FF00');
		return true;
	};

	// Зона событий
	$('.input_name').blur({text:'Имя должны быть от 3 до 32 символов может состоять только из букв и пробела'}, test_error);
	$('.input_country').blur({text:'Поле Страна должно быть от 3 до 120 и состоять из букв и пробелов'}, test_error);
	$('.input_street').blur({text:'Поле Улица, дом, квартира должно быть от 3 до 120 и состоять из букв, цифр и пробелов'}, test_error);
	$('.input_apt').blur({text:'Поле Квартира, блок должно быть от 3 до 120 и состоять из букв, цифр и пробелов'}, test_error);
	$('.input_region').blur({text:'Поле Край/Область/Регион должно быть от 3 до 120 и состоять из букв, цифр и пробелов'}, test_error);
	$('.input_city').blur({text:'Поле Город должно быть от 3 до 120 и состоять из букв, цифр и пробелов'}, test_error);
	$('.input_code').blur({text:'Поле Почтовый индекс должно быть от 3 до 120 и состоять из букв, цифр и пробелов'}, test_error);
	$('.input_phone').blur({text:'Некорректный номер телефона'}, test_error);
})