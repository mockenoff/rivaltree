import Ember from 'ember';

export default Ember.Route.extend({
	redirect(model, transition) {
		if (transition.targetName === 'brackets.index') {
			this.transitionTo('index');
		}
	},
});
