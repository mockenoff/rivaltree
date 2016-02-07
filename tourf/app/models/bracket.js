import DS from 'ember-data';

export default DS.Model.extend({
	title: DS.attr('string'),
	is_finished: DS.attr('boolean', {defaultValue: false}),
	has_third_place: DS.attr('boolean', {defaultValue: false}),
	is_double_elimination: DS.attr('boolean', {defaultValue: true}),
	teams: DS.attr({defaultValue: {}}),
	seeds: DS.attr({defaultValue: {}}),
	losers: DS.attr({defaultValue: []}),
	winners: DS.attr({defaultValue: []}),
	round_robin: DS.attr({defaultValue: []}),
	winner_loser: DS.attr({defaultValue: []}),
});
