import Ember from 'ember';

export default Ember.Route.extend({
	model(params) {
		return this.store.findRecord('bracket', params.id);
	},

	titleToken: function(model) {
		return model.get('title')+' ('+model.get('phase')[1]+')';
	},
});
