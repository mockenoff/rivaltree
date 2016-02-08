import DS from 'ember-data';
import config from '../config/environment';

export default DS.RESTAdapter.extend({
	host: config.apiURL,
	buildURL: function(type, id, record) {
		return this._super(type, id, record) + '/';
	},
	shouldReloadAll: function() {
		// Override for deprecation
		// Otherwise will only fetch from server if there are less than one record in the store
		return true;
	},
});
