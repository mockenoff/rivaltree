import Ember from 'ember';

export default Ember.Route.extend({
	model(params) {
		if (params.page_id === 'teams') {
			return this.store.query('team', {bracket_id: this.modelFor('brackets.view').id});
		}
		return this.modelFor('brackets.view');
	}
});
