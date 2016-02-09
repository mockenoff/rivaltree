import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'nav',
	classNames: ['side-nav'],
	classNameBindings: ['isShowing'],

	isShowing: false,
	pageState: Ember.inject.service('page-state'),

	init() {
		this._super(...arguments);
		this.get('pageState').set('routeName', this.get('pageState').get('routeName'));
	},

	toggleShowing() {
		if (this.get('pageState').get('routeName').startsWith('brackets') === true) {
			this.set('isShowing', true);
		} else {
			this.set('isShowing', false);
		}
	},

	pageChanged: Ember.on('init', Ember.observer('pageState.routeName', function() {
		Ember.run.once(this, 'toggleShowing');
	})),
});
