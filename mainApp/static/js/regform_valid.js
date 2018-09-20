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

	function test_repassword(){
		if( $('.input_password').val() !== $('.input_repassword').val() ){
			console.log('Пароли не совпадают');
			$(this).css('border-color', '#FF0000');
			return false;
		}

		$(this).css('border-color', '#00FF00');
		return true;
	};

	// Зона событий
	$('.input_login').blur({text:'Логин быть от 4 до 32 символов. В логине могут быть только латинские буквы, цифры и знаки "-" и "_"'}, test_error);
	$('.input_password').blur({text:'Пароль должен состатья от 8 до 72 символов содержать буквы разного регистра и хотя бы одну цифру и спец символ'}, test_error);
	$('.input_repassword').blur(test_repassword);
	$('.input_name').blur({text:'Имя должны быть от 3 до 32 символов может состоять только из букв и пробела'}, test_error);
	$('.input_surname').blur({text:'Фамилия должны быть от 3 до 32 символов может состоять только из букв и пробела'}, test_error);
	$('.input_email').blur({text:'Некорректный email'}, test_error);
	$('.input_phone').blur({text:'Некорректный номер телефона'}, test_error);
})