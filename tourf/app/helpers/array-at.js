import Ember from 'ember';

export function arrayAt(params/*, hash*/) {
	return params[1] in params[0] === true ? params[0][params[1]] : undefined;
}

export default Ember.Helper.helper(arrayAt);
