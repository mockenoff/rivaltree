import DS from 'ember-data';

export default DS.Model.extend({
	title: DS.attr('string'),
	views: DS.attr('number', {defaultValue: 0}),
	is_randomized: DS.attr('boolean', {defaultValue: false}),
	has_round_robin: DS.attr('boolean', {defaultValue: true}),
	has_third_place: DS.attr('boolean', {defaultValue: false}),
	is_double_elimination: DS.attr('boolean', {defaultValue: true}),
	phase: DS.attr({defaultValue: [1, 'New',]}),
	teams: DS.attr({defaultValue: {}}),
	seeds: DS.attr({defaultValue: {}}),
	losers: DS.attr({defaultValue: []}),
	winners: DS.attr({defaultValue: []}),
	round_robin: DS.attr({defaultValue: []}),
	winner_loser: DS.attr({defaultValue: []}),
	datetime: DS.attr('date', {defaultValue: new Date()}),
	date_created: DS.attr('date', {defaultValue: new Date()}),
	date_updated: DS.attr('date', {defaultValue: new Date()}),
});
