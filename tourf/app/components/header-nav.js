import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'header',
	classNames: ['header-nav'],

	brackets: null,
	store: Ember.inject.service('store'),
	pageState: Ember.inject.service('page-state'),
	userInfo: Ember.inject.service('user-info'),
	filterKeys: ['title', 'event_name'],

	menuOptions: [
		['settings', 'Settings'],
		['logout', 'Logout'],
	],

	init: function() {
		this._super(...arguments);

		if (this.get('userInfo').user !== null) {
			this.set('brackets', this.get('store').findAll('bracket'));
		} else {
			this.set('brackets', null);
		}
	},

	eventString: function(ev) {
		return ev.get('title') +' (' + ev.get('event_name') + ')';
	},
});
