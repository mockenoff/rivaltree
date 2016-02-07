import Ember from 'ember';

export default Ember.Service.extend({
	user: null,
	store: Ember.inject.service('store'),
	pingUser() {
		var self = this;
		return this.get('store').findRecord('user', 'self').then(function(user) {
			self.set('user', user);
		});
	}
});
