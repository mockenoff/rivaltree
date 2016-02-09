import Ember from 'ember';

export function plus(params/*, hash*/) {
	return parseInt(params[0], 10) + parseInt(params[1], 10);
}

export default Ember.Helper.helper(plus);
