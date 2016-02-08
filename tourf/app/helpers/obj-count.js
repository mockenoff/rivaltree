import Ember from 'ember';

export function objCount(params/*, hash*/) {
	var count = 0;
	for (var key in params[0]) {
		count++;
	}
	return count;
}

export default Ember.Helper.helper(objCount);
