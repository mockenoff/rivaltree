import Ember from 'ember';

export default Ember.Service.extend({
	dropdowns: [],
	currentDropdown: null,

	init() {
		this._super(...arguments);

		var self = this;
		Ember.$(document.body).click(function(ev) {
			var currentDropdown = self.get('currentDropdown');

			if (currentDropdown === null) {
				return;
			}

			var dropdowns = self.get('dropdowns');
			for (var i = 0, l = dropdowns.length; i < l; i++) {
				if (dropdowns[i].element.contains(ev.target) === true) {
					return;
				}
			}

			currentDropdown.send('toggleDropdown');
		});
	},

	toggleDropdown(dropdown) {
		var currentDropdown = this.get('currentDropdown');
		if (currentDropdown === dropdown) {
			dropdown.set('isShowing', false);
			this.set('currentDropdown', null);
		} else {
			if (currentDropdown !== null) {
				currentDropdown.set('isShowing', false);
			}
			dropdown.set('isShowing', true);
			this.set('currentDropdown', dropdown);
		}
	},

	register(dropdown) {
		this.get('dropdowns').push(dropdown);
	},

	unregister(dropdown) {
		this.get('dropdowns').splice(this.get('dropdowns').indexOf(dropdown), 1);
	},
});
