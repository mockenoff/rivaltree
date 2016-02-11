import Ember from 'ember';

export default Ember.Controller.extend({
	isSubmitting: false,
	canSubmit: Ember.computed('isSubmitting', 'model.title', 'model.teams.[]', function() {
		return this.get('isSubmitting') === true || (this.get('model.title') || '').trim() === '' || this.get('model.teams').length === 0 ? false : true;
	}),

	actions: {
		saveBracket() {
			this.set('isSubmitting', true);
			this.get('model').save().then(Ember.run.bind(this, function(data) {
				this.set('isSubmitting', false);
				this.transitionTo('brackets.view', this.model.get('id'));
			})).catch(Ember.run.bind(this, function(err) {
				this.set('isSubmitting', false);
			}));
		},
	},
});
