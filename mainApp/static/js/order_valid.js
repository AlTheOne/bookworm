$(document).ready(function(){

	function totalPrice(){
		let tp_cart = 0;
		$('.price').each(function(){
			tp_cart = tp_cart + parseFloat($(this).text());
		})
		$('#total_order_amount').text(tp_cart.toFixed(2));
	}
	totalPrice();

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