import DS from 'ember-data';

export default DS.Model.extend({
	title: DS.attr('string'),
	event_id: DS.attr('number'),
	event_name: DS.attr('string'),
	status: DS.attr('string'),
	datetime: DS.attr('date'),
	location: DS.attr('string'),
	bracket_id: DS.attr('number'),
	teams: DS.hasMany('team', {defaultValue: []}),
});
