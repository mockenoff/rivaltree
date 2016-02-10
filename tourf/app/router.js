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

    this.resource('settings', {path: '/settings/'}, function() {
        this.route('index', {path: '/'});
    });

    this.resource('brackets', {path: '/brackets/'}, function() {
        this.route('index', {path: '/'});
        this.route('fresh', {path: '/new/'});
        this.route('view', {path: '/:id'}, function() {
            this.route('page', {path: '/:page_id'});
        });
    });
});

export default Router;
