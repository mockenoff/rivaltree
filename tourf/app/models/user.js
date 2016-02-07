import DS from 'ember-data';

export default DS.Model.extend({
	name: DS.attr('string'),
	email: DS.attr('string'),
	username: DS.attr('string'),
	account_level: DS.attr({defaultValue: []}),
});
