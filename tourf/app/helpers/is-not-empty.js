import Ember from 'ember';

export function isNotEmpty(params/*, hash*/) {
	return ($.isArray(params[0]) === true && params[0].length > 0) || $.isEmptyObject(params[0]) === false;
}

export default Ember.Helper.helper(isNotEmpty);
