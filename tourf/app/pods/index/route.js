import Ember from 'ember';

export default Ember.Route.extend({
	model() {
		var self = this;
		return this.store.findAll('bracket').catch(function(err) {
			self.transitionTo('login');
		});
	},

	titleToken(model) {
		var bracketTotal = model.get('length'),
			token = 'Hello, friend!';
		if (bracketTotal === 0) {
			token += ' Let\'s get you started with some brackets!';
		} else if (bracketTotal === 1) {
			token += ' Manage your bracket and make some new ones!';
		} else {
			token += ' You\'ve got '+bracketTotal+' brackets waiting for you!';
		}
		return token;
	},
});
