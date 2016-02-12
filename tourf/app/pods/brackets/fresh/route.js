import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		return this.store.createRecord('bracket');
	},

	checkModel: function() {
		var model = this.get('controller.model');
		if (model.get('id') === null) {
			model.deleteRecord();
		}
	}.on('deactivate'),

	titleToken: 'Create a bracket',
});
