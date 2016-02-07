import Ember from 'ember';

export default Ember.Component.extend({
	classNames: ['modal'],
	classNameBindings: ['isShowing'],

	isShowing: true,

	didInsertElement() {
		this.get('element').setAttribute('tabindex', '0');
		this._super(...arguments);
	},

	click(ev) {
		if (ev.target === this.get('element')) {
			this._actions['toggleShow'].apply(this);
		}
	},

	keyDown(ev) {
		var keyCode = ev.keyCode || ev.which;
		if (ev.target.tagName.toLowerCase() !== 'input' && keyCode === 27) {
			this._actions['toggleShow'].apply(this);
			this.get('element').blur();
		}
	},

	actions: {
		toggleShow() {
			this.toggleProperty('isShowing');
			if (this.get('isShowing') === true) {
				this.get('element').focus();
			}
		},
	},
});
