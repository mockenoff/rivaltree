import Ember from 'ember';

export default Ember.View.extend({
	classNames: ['container'],

	showSide: false,
	pageState: Ember.inject.service('page-state'),

	init() {
		this._super(...arguments);
		this.get('pageState').set('routeName', this.get('pageState').get('routeName'));
	},

	pageChanged: Ember.on('init', Ember.observer('pageState.routeName', function() {
		console.log('CHANGED', this.get('pageState.routeName'));
		if (this.get('pageState').get('routeName').startsWith('brackets') === true) {
			this.set('showSide', true);
		} else {
			this.set('showSide', false);
		}
	})),
});
