import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'header',
	classNames: ['header-nav'],

	events: null,
	store: Ember.inject.service('store'),
	pageState: Ember.inject.service('page-state'),
	filterKeys: ['title', 'event_name'],

	init: function() {
		this._super(...arguments);
		// this.set('events', this.get('store').findAll('event'));
	},

	eventString: function(ev) {
		return ev.get('title') +' (' + ev.get('event_name') + ')';
	},
});
