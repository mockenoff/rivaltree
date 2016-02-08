import Ember from 'ember';

export default Ember.Controller.extend({
	filterInput: '',

	filteredBrackets: function(){
		var brackets = this.get('model'),
			filterInput = this.get('filterInput'),
			regex = new RegExp(filterInput, 'gi');

		return brackets.filter(function(br){
			return regex.test(br.get('title'));
		});
	}.property('filterInput'),

	statusCounts: function(){
		var status = null,
			statusCounts = {};
		this.get('model').forEach(function(br){
			status = br.get('is_finished') === true ? 'finished' : 'ongoing';
			if (statusCounts[status] === undefined) {
				statusCounts[status] = 0;
			}
			statusCounts[status]++;
		});
		return statusCounts;
	}.property('model'),
});
