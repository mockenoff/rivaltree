import Ember from 'ember';
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
		if (Ember.$.isEmptyObject(needle) === false) {
			for (var i = 0, l = haystack.length; i < l; i++) {
				if (haystack[i].team1.seed === needle.seed || haystack[i].team2.seed === needle.seed) {
					return haystack[i];
				}
			}
		}
		return null;
	},

	normalizeBracket(bracket) {
		var self = this;

		['winners', 'losers'].forEach(function(key) {
			var gameTotal = 0,
				nextRound = null,
				newGames = null;

			for (var i = 0, l = bracket[key].length; i < l; i++) {
				if (i > 0) {
					newGames = [];
					gameTotal = Math.pow(2, i - 1);
					nextRound = bracket[key][i - 1];

					for (var j = 0; j < gameTotal; j++) {
						if (nextRound[j]) {
							newGames.push(self.findMatchingGame(bracket[key][i], nextRound[j].team1));
							newGames.push(self.findMatchingGame(bracket[key][i], nextRound[j].team2));
						} else {
							newGames.push(null, null);
						}
					}

					bracket[key][i] = newGames;
				}
			}
		});

		['winners', 'losers', 'winner_loser', 'round_robin'].forEach(function(key) {
			if (Ember.$.isArray(bracket[key]) === true) {
				bracket[key] = bracket[key].reverse();
			}
		});

		return bracket;
	},

	normalizeResponse(store, primaryModelClass, payload, id, requestType) {
		var self = this;

		if ('brackets' in payload) {
			payload.brackets.forEach(function(bracket, idx) {
				payload.brackets[idx] = self.normalizeBracket(bracket);
			});
		}

		if ('bracket' in payload) {
			payload.bracket = this.normalizeBracket(payload.bracket);
		}

		return this._super(...arguments);
	},
});
