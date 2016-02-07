import Ember from 'ember';

export default Ember.Controller.extend({
	filterInput: '',

	filteredEvents: function(){
		var events = this.get('model'),
			filterInput = this.get('filterInput'),
			regex = new RegExp(filterInput, 'gi');

		return events.filter(function(ev){
			return regex.test(ev.get('title')) || regex.test(ev.get('event_name'));
		});
	}.property('filterInput'),

	statusCounts: function(){
		var status = null,
			statusCounts = {};
		this.get('model').forEach(function(ev){
			status = ev.get('status');
			if (statusCounts[status] === undefined) {
				statusCounts[status] = 0;
			}
			statusCounts[status]++;
		});
		return statusCounts;
	}.property('model'),
});
