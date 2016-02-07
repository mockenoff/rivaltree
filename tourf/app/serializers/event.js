import DS from 'ember-data';

export default DS.RESTSerializer.extend(DS.EmbeddedRecordsMixin, {
	attrs: {
		teams: {
			serialize: false,
			deserialize: 'records',
		},
	},
	isNewSerializerAPI: true,
});
