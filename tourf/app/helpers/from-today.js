import Ember from 'ember';

export function fromToday(params/*, hash*/) {
	return Math.round((params[0] - (new Date())) / (1000*60*60*24));
}

export default Ember.Helper.helper(fromToday);
