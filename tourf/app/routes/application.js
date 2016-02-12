import Ember from 'ember';

export default Ember.Route.extend({
	title(tokens) {
		var title = 'rivaltree';
		if (Ember.$.isArray(tokens) === false) {
			tokens = [title];
		} else {
			tokens.push(title);
		}
		return tokens.join(' | ');
	},
});
