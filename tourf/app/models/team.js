import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr('string'),
	seed: DS.attr('number'),
	logo: DS.attr('string'),
	cover: DS.attr('string'),
	location: DS.attr('string'),
	region_id: DS.attr('number'),
	region_name: DS.attr('string'),
});
