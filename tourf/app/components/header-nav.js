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

	bracketString: function(br) {
		return br.get('title') +' (' + (br.get('is_finished') === true ? 'finished' : 'ongoing') + ')';
	},

	refreshBrackets() {
		if (this.get('userInfo').user !== null) {
			this.set('brackets', this.get('store').findAll('bracket'));
		} else {
			this.set('brackets', null);
		}
	},

	userChanged: Ember.observer('userInfo.user', function() {
		Ember.run.once(this, 'refreshBrackets');
	}),
});
