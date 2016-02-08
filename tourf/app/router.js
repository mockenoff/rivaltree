import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
    rootURL: config.rootURL,
    location: config.locationType,

    pageState: Ember.inject.service('page-state'),
    userInfo: Ember.inject.service('user-info'),

    updateState: function() {
        var self = this;

        this.get('userInfo').pingUser().then(function() {
            if (self.currentRouteName === 'login') {
                self.transitionTo('index');
            }
        }).catch(function(err) {
            if (parseInt(err.errors[0].status, 10) === 401) {
                self.get('userInfo').set('user', null);
                self.transitionTo('login');
            }
        });

        this.get('pageState').updateRoute(this);
    }.on('didTransition'),
});

Router.map(function() {
    this.route('login', {path: '/login/'});
    this.route('logout', {path: '/logout/'});
    this.route('settings', {path: '/settings/:page_id'});

    this.route('brackets', function() {
    	this.route('index', {path: '/:id'});
    	this.route('page', {path: '/:id/:page_id'});
    });
});

export default Router;
