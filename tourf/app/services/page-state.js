import Ember from 'ember';

export default Ember.Service.extend({
	params: null,
	routeName: null,
	updateRoute(router) {
		this.set('routeName', router.currentRouteName);
		this.set('params', router.currentState.routerJsState.params[router.currentRouteName]);
	},
});
