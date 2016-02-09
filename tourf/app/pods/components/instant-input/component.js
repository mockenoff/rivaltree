import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'input',
	classNames: ['instant-input'],

	type: 'text',
	value: null,
	attributeBindings: ['type', 'value'],

	model: null,
	alwaysSave: true,
	cleanProperty: null,

	didInsertElement() {
		this._super(...arguments);

		this.element.addEventListener('focus', Ember.run.bind(this, this.get('focusEvent')));
		this.element.addEventListener('blur', Ember.run.bind(this, this.get('blurEvent')));
	},

	willDestroyElement() {
		this._super(...arguments);

		this.element.removeEventListener('focus', this.get('focusEvent'));
		this.element.removeEventListener('blur', this.get('blurEvent'));
	},

	focusEvent() {
		this.set('cleanProperty', this.get('value'));
	},

	blurEvent() {
		var value = this.element.value,
			cleanProperty = this.get('cleanProperty');

		if (value !== cleanProperty) {
			this.set('value', value);

			if (this.get('alwaysSave') === true) {
				this.get('model').save();
			}
		}
	},
});
