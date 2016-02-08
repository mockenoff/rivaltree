import Ember from 'ember';

export default Ember.Controller.extend({
	isShowing: false,
	isSubmitting: false,
	formError: false,

	team1Wins: 0,
	team2Wins: 0,
	currentGame: null,

	team1WinsError: function() {
		var team1Wins = this.get('team1Wins'),
			parsedWins = parseInt(team1Wins, 10);
		if (/\D/.test(team1Wins) === true || isNaN(parsedWins) === true) {
			return 'Must be a number';
		} else if (parsedWins < 0) {
			return 'Must be greater than zero';
		}
		return false;
	}.property('team1Wins'),

	team2WinsError: function() {
		var team2Wins = this.get('team2Wins'),
			parsedWins = parseInt(team2Wins, 10);
		if (/\D/.test(team2Wins) === true || isNaN(parsedWins) === true) {
			return 'Must be a number';
		} else if (parsedWins < 0) {
			return 'Must be greater than zero';
		}
		return false;
	}.property('team2Wins'),

	actions: {
		openForm(game) {
			this.set('currentGame', game);
			this.set('team1Wins', game.team1.wins);
			this.set('team2Wins', game.team2.wins);
			this.set('isShowing', true);
		},

		saveForm(game) {
			var self = this;
			if (this.get('isSubmitting') === false && this.get('team1WinsError') === false && this.get('team2WinsError') === false) {
				this.set('formError', false);
				this.set('isSubmitting', true);

				this.store.findRecord('game', game.id).then(function(foundGame) {
					foundGame.set('team1_wins', self.get('team1Wins'));
					foundGame.set('team2_wins', self.get('team2Wins'));
					foundGame.save().then(function() {
						self.set('isSubmitting', false);
					}, function(err) {
						self.set('isSubmitting', false);
						if (err.message) {
							self.set('formError', err.message);
						}
					});
				}, function(err) {
					self.set('isSubmitting', false);
					if (err.message) {
						self.set('formError', err.message);
					}
				});
			}
		},
	},
});
