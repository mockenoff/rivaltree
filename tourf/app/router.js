import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
	rootURL: config.rootURL,
	location: config.locationType,

	pageState: Ember.inject.service('page-state'),
	userInfo: Ember.inject.service('user-info'),

	updateState: function() {
		var self = this;
		this.get('userInfo').pingUser().then(function(user) {
			if (self.currentRouteName === 'login') {
				self.transitionTo('index');
			}
		}).catch(function(err) {
			if (err.errors[0].status == 401) {
				self.get('userInfo').set('user', null);
				self.transitionTo('login');
			}
		});

		this.get('pageState').updateRoute(this);
	}.on('didTransition'),
});

Router.map(function() {
	this.route('login', {path: '/login/'});
	this.route('events', {path: '/events/:id'});
	this.route('brackets', {path: '/brackets/:id'});
});

export default Router;
