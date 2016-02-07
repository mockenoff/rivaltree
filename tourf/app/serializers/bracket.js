import DS from 'ember-data';

export default DS.RESTSerializer.extend(DS.EmbeddedRecordsMixin, {
	isNewSerializerAPI: true,
	attrs: {
		teams: {
			deserialize: 'records',
			serialize: 'records',
		},
	},
	findMatchingGame(haystack, needle) {
		if ($.isEmptyObject(needle) === false) {
			for (var i = 0, l = haystack.length; i < l; i++) {
				if (haystack[i].team1.seed === needle.seed || haystack[i].team2.seed === needle.seed) {
					return haystack[i];
				}
			}
		}
		return null;
	},
	normalizeResponse(store, primaryModelClass, payload, id, requestType) {
		var self = this;

		['winners', 'losers'].forEach(function(key) {
			var gameTotal = 0,
				nextRound = null,
				newGames = null;

			for (var i = 0, l = payload.bracket[key].length; i < l; i++) {
				if (i > 0) {
					newGames = [];
					gameTotal = Math.pow(2, i - 1);
					nextRound = payload.bracket[key][i - 1];

					for (var j = 0; j < gameTotal; j++) {
						if (nextRound[j]) {
							newGames.push(self.findMatchingGame(payload.bracket[key][i], nextRound[j].team1));
							newGames.push(self.findMatchingGame(payload.bracket[key][i], nextRound[j].team2));
						} else {
							newGames.push(null, null);
						}
					}

					payload.bracket[key][i] = newGames;
				}
			}
		});

		['winners', 'losers', 'winner_loser', 'round_robin'].forEach(function(key) {
			if ($.isArray(payload.bracket[key]) === true) {
				payload.bracket[key] = payload.bracket[key].reverse();
			}
		});

		return this._super(...arguments);
	},
});
