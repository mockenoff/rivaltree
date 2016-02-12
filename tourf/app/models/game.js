import DS from 'ember-data';

export default DS.Model.extend({
	group: DS.attr({defaultValue: [1, 'Winner',]}),
	round: DS.attr('number'),
	number: DS.attr('number'),
	bracket_id: DS.attr('number'),
	team1_id: DS.attr('number'),
	team1_seed: DS.attr('number'),
	team1_wins: DS.attr('number'),
	team2_id: DS.attr('number'),
	team2_seed: DS.attr('number'),
	team2_wins: DS.attr('number'),
});
