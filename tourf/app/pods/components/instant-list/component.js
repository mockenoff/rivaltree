import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'div',
	inputElement: null,
	classNames: ['instant-list'],

	model: null,
	alwaysSave: true,
	isSubmitting: false,
	isMoving: false,

	inputValue: '',
	mousePosition: [0, 0],
	placeholder: 'Add item',
	currentTarget: null,

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
		if (ev.target.nodeName !== 'LI') {
			return;
		}

		Ember.$(document.body).addClass('no-select');

		this.set('isMoving', true);
		this.set('currentTarget', ev.target);
		this.set('mousePosition', [ev.clientX, ev.clientY]);
		document.addEventListener('mousemove', this.get('moveEvent'));
	},

	upEvent(ev) {
		if (this.get('isMoving') === false) {
			return;
		}

		Ember.$(document.body).removeClass('no-select');

		var currentTarget = this.get('currentTarget');
		currentTarget.style.top = 0;
		currentTarget.style.left = 0;

		this.set('isMoving', false);
		document.removeEventListener('mousemove', this.get('moveEvent'));
	},

	moveEvent(ev) {
		if (this.get('isMoving') === false) {
			return;
		}

		var mousePosition = this.get('mousePosition'),
			currentTarget = this.get('currentTarget');

		currentTarget.style.left = (ev.clientX - mousePosition[0])+'px';
		currentTarget.style.top = (ev.clientY - mousePosition[1])+'px';
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
				for (var i = 0, l = list.length; i < l; i++) {
					if (value === list[i]) {
						inputElement.value = '';
						return; // BUG: feedback on duplicates?
					}
				}

				list.pushObject(value);
				this.set('value', list);

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
