import Ember from 'ember';

export default Ember.Service.extend({
	user: null,
	store: Ember.inject.service('store'),
	pingUser() {
		return this.get('store').findAll('user').then(Ember.run.bind(this, function(users) {
			if (users.get('length') > 0) {
				this.set('user', users.objectAt(0));
			} else {
				this.set('user', null);
			}
		}));
	}
});
