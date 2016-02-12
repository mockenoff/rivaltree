import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'div',
	inputElement: null,
	classNames: ['instant-check'],

	model: null,
	alwaysSave: true,
	isSubmitting: false,

	didInsertElement() {
		this._super(...arguments);
		this.set('inputElement', this.element.querySelector('input[type="checkbox"]'));
	},

	actions: {
		changeEvent() {
			this.set('value', this.get('inputElement').checked);

			if (this.get('alwaysSave') === true) {
				this.set('isSubmitting', true);
				this.get('model').save().then(Ember.run.bind(this, function() {
					this.set('isSubmitting', false);
				})).catch(Ember.run.bind(this, function(err) {
					this.set('isSubmitting', false); // BUG: show error feedback
				}));
			}
		},
	},
});
