import Ember from 'ember';

export function orCheck(params/*, hash*/) {
	for (var i = 0, l = params.length; i < l; i++) {
		if (params[i]) {
			return true;
		}
	}
	return false;
}

export default Ember.Helper.helper(orCheck);
