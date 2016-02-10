import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'div',
	inputElement: null,
	classNames: ['instant-list'],
	classNameBindings: ['isSortable:sortable', 'isMoving:moving'],

	model: null,
	alwaysSave: true,
	isSortable: true,
	isSubmitting: false,
	lockVertical: true,
	isMoving: false,

	inputValue: '',
	mousePosition: [0, 0],
	placeholder: 'Add item',
	currentTarget: null,
	itemElements: null,

	didInsertElement() {
		this._super(...arguments);

		if (Ember.$.isArray(this.get('value')) === false) {
			this.set('value', []);
		}

		this.set('inputElement', this.element.querySelector('input[type="text"]'));

		this.set('downEvent', Ember.run.bind(this, this.get('downEvent')));
		this.set('upEvent', Ember.run.bind(this, this.get('upEvent')));
		this.set('moveEvent', Ember.run.bind(this, this.get('moveEvent')));

		this.element.addEventListener('mousedown', this.get('downEvent'));
		document.addEventListener('mouseup', this.get('upEvent'));
	},

	willDestroyElement() {
		this._super(...arguments);

		this.element.removeEventListener('mousedown', this.get('downEvent'));
		document.removeEventListener('mouseup', this.get('upEvent'));
	},

	downEvent(ev) {
		if (ev.target.nodeName === 'I' && ev.target.classList.contains('fa-times') === true) {
			this.get('value').removeObject(ev.target.parentElement.dataset.item);
		} else if (this.get('isSortable') === true && ev.target.nodeName === 'LI') {
			document.body.classList.add('no-select');
			ev.target.classList.add('current');

			this.set('isMoving', true);
			this.set('currentTarget', ev.target);
			this.set('mousePosition', [ev.clientX, ev.clientY]);
			document.addEventListener('mousemove', this.get('moveEvent'));

			var itemElements = [],
				items = this.element.querySelectorAll('li[data-item]');
			for (var i = 0, l = items.length; i < l; i++) {
				itemElements.push({element: items[i], rect: items[i].getBoundingClientRect()});
			}
			this.set('itemElements', itemElements);
		}
	},

	upEvent(ev) {
		if (this.get('isMoving') === false) {
			return;
		}

		var newOrder = [],
			itemElements = this.get('itemElements'),
			currentTarget = this.get('currentTarget'),
			currentIndex = parseInt(currentTarget.dataset.index, 10);

		for (var i = 0, l = itemElements.length; i < l; i++) {
			if (currentIndex === i) {
				newOrder.push({element: currentTarget, rect: currentTarget.getBoundingClientRect()});
			} else {
				newOrder.push(itemElements[i]);
			}
			itemElements[i].element.style.top = 0;
			itemElements[i].element.style.left = 0;
		}

		newOrder.sort(function(a, b) {
			return a.rect.top < b.rect.top ? -1 : 1;
		});

		var value = this.get('value');
		value.length = 0;
		for (i = 0, l = newOrder.length; i < l; i++) {
			value.pushObject(newOrder[i].element.dataset.item);
		}

		this.set('isMoving', false);
		document.removeEventListener('mousemove', this.get('moveEvent'));

		currentTarget.classList.remove('current');
		document.body.classList.remove('no-select');
	},

	moveEvent(ev) {
		if (this.get('isMoving') === false) {
			return;
		}

		var mousePosition = this.get('mousePosition'),
			currentTarget = this.get('currentTarget'),
			currentIndex = parseInt(currentTarget.dataset.index, 10);

		currentTarget.style.top = (ev.clientY - mousePosition[1])+'px';
		if (this.get('lockVertical') === false) {
			currentTarget.style.left = (ev.clientX - mousePosition[0])+'px';
		}

		var itemElements = this.get('itemElements');
		for (var i = 0, l = itemElements.length; i < l; i++) {
			if (i < currentIndex) {
				if (ev.clientY < (itemElements[i].rect.top + (itemElements[i].rect.height * 0.5))) {
					itemElements[i].element.style.top = itemElements[i].rect.height+'px';
				} else {
					itemElements[i].element.style.top = 0;
				}
			} else if (i > currentIndex) {
				if (ev.clientY > (itemElements[i].rect.top - (itemElements[i].rect.height * 0.5))) {
					itemElements[i].element.style.top = -itemElements[i].rect.height+'px';
				} else {
					itemElements[i].element.style.top = 0;
				}
			}
		}
	},

	actions: {
		escInput(ev) {
			this.get('inputElement').value = '';
			this.get('inputElement').blur();
		},
		enterInput(ev) {
			var inputElement = this.get('inputElement'),
				value = (inputElement.value || '').trim();

			if (value !== '') {
				var list = this.get('value');
				if (list.contains(value) === true) {
					inputElement.value = '';
					return; // BUG: feedback on duplicates?
				}

				list.pushObject(value);

				if (this.get('alwaysSave') === true) {
					this.set('isSubmitting', true);
					this.get('model').save().then(Ember.run.bind(this, function() {
						this.set('isSubmitting', false);
					})).catch(Ember.run.bind(this, function(err) {
						this.set('isSubmitting', false); // BUG: show error feedback
					}));
				}
			}

			inputElement.value = '';
		},
	},
});
