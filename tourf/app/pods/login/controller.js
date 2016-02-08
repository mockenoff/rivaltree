import Ember from 'ember';
import config from '../../config/environment';

export default Ember.Controller.extend({
	isSubmitting: false,
	formError: false,

	formData: {
		username: null,
		password: null,
	},

	actions: {
		tryLogin(data) {
			if (this.get('isSubmitting') === false) {
				this.set('formError', false);
				this.set('isSubmitting', true);

				var self = this;
				Ember.$.post(config.apiURL + '/users/login/', data).then(function() {
					self.set('isSubmitting', false);
					self.transitionTo('index');
				}, function(err) {
					self.set('isSubmitting', false);

					if (err.status === 401) {
						self.set('formError', 'Incorrect login credentials');
					} else {
						// Some other error
					}
				});
			}
		},
	},

	init() {
		this._super(...arguments);
		Ember.run.schedule('afterRender', this, function() {
			Ember.$('input[type="text"]').focus();
		});
	},
});
