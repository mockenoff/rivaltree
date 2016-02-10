import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'div',
	inputElement: null,
	classNames: ['instant-input'],

	model: null,
	alwaysSave: true,
	isSubmitting: false,
	cleanProperty: null,

	didInsertElement() {
		this._super(...arguments);

		var inputElement = this.element.querySelector('input[type="text"]');
		inputElement.addEventListener('focus', Ember.run.bind(this, this.get('focusEvent')));
		inputElement.addEventListener('blur', Ember.run.bind(this, this.get('blurEvent')));
		this.set('inputElement', inputElement);
	},

	willDestroyElement() {
		this._super(...arguments);

		var inputElement = this.get('inputElement');
		inputElement.removeEventListener('focus', this.get('focusEvent'));
		inputElement.removeEventListener('blur', this.get('blurEvent'));
	},

	focusEvent() {
		this.set('cleanProperty', this.get('value'));
	},

	blurEvent() {
		var inputElement = this.get('inputElement'),
			value = (inputElement.value || '').trim(),
			cleanProperty = this.get('cleanProperty');

		if (value === '') {
			inputElement.value = cleanProperty !== null && cleanProperty !== undefined ? cleanProperty : '';
		} else if (value !== cleanProperty) {
			this.set('value', value);

			if (this.get('alwaysSave') === true) {
				this.set('isSubmitting', true);
				this.get('model').save().then(Ember.run.bind(this, function() {
					this.set('isSubmitting', false);
				})).catch(Ember.run.bind(this, function(err) {
					this.set('isSubmitting', false); // BUG: show error feedback
				}));
			}
		}
	},

	actions: {
		escInput() {
			var inputElement = this.get('inputElement');
			inputElement.value = this.get('cleanProperty');
			inputElement.blur();
		},
		enterInput() {
			this.get('inputElement').blur();
		},
	},
});
