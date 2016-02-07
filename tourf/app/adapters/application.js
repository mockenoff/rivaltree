import DS from 'ember-data';
import config from '../config/environment';

export default DS.RESTAdapter.extend({
	host: config.apiURL,
	buildURL: function(type, id, record) {
		return this._super(type, id, record) + '/';
	},
});
