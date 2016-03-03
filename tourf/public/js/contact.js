var contactForm = document.querySelector('.contact-form'),
	nameInput = contactForm.querySelector('input[type="text"]'),
	emailInput = contactForm.querySelector('input[type="email"]'),
	messageInput = contactForm.querySelector('textarea'),
	formSubmit = contactForm.querySelector('.btn'),
	emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

nameInput.addEventListener('focus', function(ev) {
	nameInput.classList.remove('error');
});

emailInput.addEventListener('focus', function(ev) {
	emailInput.classList.remove('error');
});

messageInput.addEventListener('focus', function(ev) {
	messageInput.classList.remove('error');
});

contactForm.addEventListener('submit', function(ev) {
	var doSubmit = true;

	nameInput.classList.remove('error');
	nameInput.value = nameInput.value.trim();
	if (nameInput.value.trim() === '') {
		doSubmit = false;
		nameInput.classList.add('error');
	}

	emailInput.classList.remove('error');
	emailInput.value = emailInput.value.trim();
	if (emailInput.value.trim() === '' || emailRegex.test(emailInput.value) === false) {
		doSubmit = false;
		emailInput.classList.add('error');
	}

	messageInput.classList.remove('error');
	messageInput.value = messageInput.value.trim();
	if (messageInput.value.trim() === '') {
		doSubmit = false;
		messageInput.classList.add('error');
	}

	if (doSubmit === false) {
		ev.preventDefault();
	} else {
		formSubmit.disabled = true;
	}
});
