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
	placeholder: 'Add item',

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
		console.log('DOWN', ev);
		this.set('isMoving', true);
		document.addEventListener('mousemove', this.get('moveEvent'));
	},

	upEvent(ev) {
		console.log('UP', ev);
		this.set('isMoving', false);
		document.removeEventListener('mousemove', this.get('moveEvent'));
	},

	moveEvent(ev) {
		console.log('MOVE', ev);
	},

	actions: {
		escInput(ev) {
			this.get('inputElement').value = '';
		},
		enterInput(ev) {
			var inputElement = this.get('inputElement'),
				value = (inputElement.value || '').trim();

			if (value !== '') {
				var list = this.get('value');
				console.log('PUSH', value, list);
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
