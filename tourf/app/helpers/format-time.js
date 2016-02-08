import Ember from 'ember';

export function formatTime(params/*, hash*/) {
	var hours = params[0].getHours(),
		minutes = String(params[0].getMinutes()),
		seconds = String(params[0].getSeconds()),
		suffix = hours >= 12 ? 'PM' : 'AM';

	if (minutes.length < 2) {
		minutes = '0' + minutes;
	}
	if (seconds.length < 2) {
		seconds = '0' + seconds;
	}
	if (hours > 12) {
		hours = hours - 12;
	}
	return (hours === 0 ? 12 : hours) + ':' + minutes + ':' + seconds + ' ' + suffix;
}

export default Ember.Helper.helper(formatTime);
