import Ember from 'ember';

export default Ember.Service.extend({
	params: null,
	routeName: null,
	updateRoute(router) {
		this.set('routeName', router.currentRouteName);

		var params = {},
			routerParams = router.currentState.routerJsState.params;

		for (var route in routerParams) {
			if (route.startsWith('__') === false && route.endsWith('__') === false) {
				for (var key in routerParams[route]) {
					if (key.startsWith('__') === false && key.endsWith('__') === false) {
						params[key] = routerParams[route][key];
					}
				}
			}
		}
		this.set('params', params);
	},
});
