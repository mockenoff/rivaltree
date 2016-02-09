import Ember from 'ember';

export default Ember.Route.extend({
	model(params) {
		var bracket = this.modelFor('brackets.view');
		if (bracket.get('phase')[0] === 1) {
			this.transitionTo('brackets.view');
		} else if (params.page_id === 'teams') {
			return this.store.query('team', {bracket_id: bracket.id});
		}
	}
});
