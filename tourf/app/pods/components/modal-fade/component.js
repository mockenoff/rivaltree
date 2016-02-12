import Ember from 'ember';

export default Ember.Component.extend({
	classNames: ['modal'],
	classNameBindings: ['isShowing'],

	tabindex: 0,
	attributeBindings: ['tabindex'],

	isShowing: true,

	click(ev) {
		if (ev.target === this.element) {
			this._actions['toggleShow'].apply(this);
		}
	},

	keyDown(ev) {
		var keyCode = ev.keyCode || ev.which;
		if (ev.target.tagName.toLowerCase() !== 'input' && keyCode === 27) {
			this._actions['toggleShow'].apply(this);
			this.element.blur();
		}
	},

	toggleShow: Ember.observer('isShowing', function() {
		if (this.get('isShowing') === true) {
			this.element.focus();
		}
	}),

	actions: {
		toggleShow() {
			this.toggleProperty('isShowing');
		},
	},
});
