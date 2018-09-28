$(document).ready(function(){

	// Зона функций
	function test_error(data){
		let variable = $(this).val();
		let reg = new RegExp($(this).attr('pattern'));

		attr_class = $(this)[0].attributes.class.nodeValue;
		att = '.'+attr_class+'_error';

		if(reg.test(variable) === false){
			$(this).css('border-color', '#FF0000');
			$(att).text(data.data.text);
			return false;
		}

		$(this).css('border-color', '#00FF00');
		$(att).text('');
		return true;
	};

	function test_repassword(){
		attr_class = $(this)[0].attributes.class.nodeValue;
		att = '.'+attr_class+'_error';
		if( $('.input_password').val() !== $('.input_repassword').val() ){
			$(this).css('border-color', '#FF0000');
			$(att).text('Пароли не совпадают');
			return false;
		}

		$(this).css('border-color', '#00FF00');
		$(att).text('');
		return true;
	};

	// Зона событий
	$('.reg_input_login').blur({text:'Логин быть от 4 до 32 символов. В логине могут быть только латинские буквы, цифры и знаки "-" и "_"'}, test_error);
	$('.reg_input_password').blur({text:'Пароль должен состатья от 8 до 72 символов содержать буквы разного регистра и хотя бы одну цифру и спец символ'}, test_error);
	$('.reg_input_repassword').blur(test_repassword);
	$('.reg_input_name').blur({text:'Имя должны быть от 3 до 32 символов может состоять только из букв и пробела'}, test_error);
	$('.reg_input_surname').blur({text:'Фамилия должны быть от 3 до 32 символов может состоять только из букв и пробела'}, test_error);
	$('.reg_input_email').blur({text:'Некорректный email'}, test_error);
	$('.reg_input_phone').blur({text:'Некорректный номер телефона'}, test_error);
})