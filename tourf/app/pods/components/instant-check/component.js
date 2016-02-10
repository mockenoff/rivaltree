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

		var inputElement = this.element.querySelector('input[type="checkbox"]');
		this.set('inputElement', inputElement);
		this.element.querySelector('label').setAttribute('for', inputElement.id);

		this.set('changeEvent', Ember.run.bind(this, this.get('changeEvent')));
		inputElement.addEventListener('change', this.get('changeEvent'));
	},

	willDestroyElement() {
		this._super(...arguments);
		this.get('inputElement').removeEventListener('change', this.get('changeEvent'));
	},

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
});
