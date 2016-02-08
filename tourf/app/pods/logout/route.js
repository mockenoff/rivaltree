import Ember from 'ember';
import config from '../../config/environment';

export default Ember.Route.extend({
	setupController() {
		var self = this;
		Ember.$.post(config.apiURL + '/users/logout/').then(function() {
			self.transitionTo('login');
		});
	},
});
