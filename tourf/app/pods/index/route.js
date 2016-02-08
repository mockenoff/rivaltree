import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		var self = this;
		return this.store.findAll('bracket').catch(function(err) {
			self.transitionTo('login');
		});
	}
});
