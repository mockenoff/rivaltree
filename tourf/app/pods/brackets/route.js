import Ember from 'ember';

export default Ember.Route.extend({
	model(params) {
		if (params.id !== undefined) {
			return this.store.findRecord('bracket', params.id);
		}
	}
});
