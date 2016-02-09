import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr('string'),
	starting_seed: DS.attr('number'),
	header_path: DS.attr('string'),
	win: DS.attr('number'),
	loss: DS.attr('number'),
});
