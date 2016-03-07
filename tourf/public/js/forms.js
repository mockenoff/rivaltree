(function(){
	var formList = document.querySelectorAll('form'),
		inputList = [],
		submitList = [],
		emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

	function focusEvent(ev) {
		ev.target.classList.remove('error');
	}

	function submitEvent(ev) {
		var doSubmit = true,
			formId = ev.target.dataset['form'],
			inputs = inputList[formId];

		for (var i = 0, l = inputs.length; i < l; i++) {
			inputs[i].classList.remove('error');
			inputs[i].value = inputs[i].value.trim();
			if (inputs[i].value === '' || (inputs[i].type === 'email' && emailRegex.test(inputs[i].value) === false) || (inputs[i].type === 'password' && inputs[i].value.length < 6)) {
				doSubmit = false;
				inputs[i].classList.add('error');
			}
		}

		if (doSubmit === false) {
			ev.preventDefault();
		} else {
			submitList[formId].disabled = true;
		}
	}

	for (var i = 0, l = formList.length; i < l; i++) {
		formList[i].dataset['form'] = i;
		formList[i].addEventListener('submit', submitEvent);

		submitList[i] = formList[i].querySelector('input[type="submit"]');
		inputList[i] = formList[i].querySelectorAll('input:not([type="hidden"]), textarea');

		for (var j = 0, k = inputList[i].length; j < k; j++) {
			inputList[i][j].addEventListener('focus', focusEvent);
		}
	}
})();
