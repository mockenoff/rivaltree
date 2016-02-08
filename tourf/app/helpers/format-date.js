import Ember from 'ember';

export function formatDate(params/*, hash*/) {
	var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
	return months[params[0].getMonth()] + ' ' + params[0].getDate() + ', ' + params[0].getFullYear();
}

export default Ember.Helper.helper(formatDate);
