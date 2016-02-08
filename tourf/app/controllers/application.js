import Ember from 'ember';

export default Ember.Controller.extend({
	showSide: false,
	pageState: Ember.inject.service('page-state'),

	init() {
		this._super(...arguments);
		this.get('pageState').set('routeName', this.get('pageState').get('routeName'));
	},

	setShow() {
		var routeName = this.get('pageState').get('routeName');
		if (typeof routeName === 'string' && routeName.startsWith('brackets') === true) {
			this.set('showSide', true);
		} else {
			this.set('showSide', false);
		}
		console.log('CHANGED', routeName, this.get('showSide'));
	},

	pageChanged: Ember.on('init', Ember.observer('pageState.routeName', function() {
		Ember.run.once(this, 'setShow');
	})),
});
