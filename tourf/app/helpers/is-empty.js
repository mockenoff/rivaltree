import Ember from 'ember';

export function isEmpty(params/*, hash*/) {
	return $.isEmptyObject(params[0]) === true || ($.isArray(params[0]) === true && params[0].length === 0);
}

export default Ember.Helper.helper(isEmpty);
