import DS from 'ember-data';

export default DS.Model.extend({
	title: DS.attr('string'),
	views: DS.attr('number', {defaultValue: 0}),
	has_third_place: DS.attr('boolean', {defaultValue: false}),
	is_double_elimination: DS.attr('boolean', {defaultValue: true}),
	phase: DS.attr({defaultValue: []}),
	teams: DS.attr({defaultValue: {}}),
	team_ids: DS.attr({defaultValue: []}),
	seeds: DS.attr({defaultValue: {}}),
	losers: DS.attr({defaultValue: []}),
	winners: DS.attr({defaultValue: []}),
	round_robin: DS.attr({defaultValue: []}),
	winner_loser: DS.attr({defaultValue: []}),
	datetime: DS.attr('date'),
	date_created: DS.attr('date'),
	date_updated: DS.attr('date'),
});
