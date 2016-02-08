import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'ul',
	classNames: ['dropdown'],
	classNameBindings: ['isShowing'],
	dropdownService: Ember.inject.service('dropdownService'),

	items: null,
	inputValue: '',
	isShowing: false,
	filterInput: null,
	isFiltered: false,
	filterKeys: null,
	defaultItem: null,
	currentID: null,
	keyID: 'id',

	init() {
		this._super(...arguments);

		var classNames = this.get('class');
		if (typeof classNames === 'string') {
			this.get('classNames').pushObjects(classNames.split(' '));
		}

		this.get('dropdownService').register(this);
	},

	willDestroyElement() {
		this._super(...arguments);
		this.get('dropdownService').unregister(this);
	},

	currentItem: Ember.computed('currentID', 'items.[]', function() {
		var items = this.get('items'),
			keyID = this.get('keyID'),
			currentID = this.get('currentID');

		for (var i = 0, l = items.get('length'); i < l; i++) {
			var item = items.objectAt(i);
			if (Ember.$.isArray(item) === true) {
				if (item[0] === currentID) {
					return item[1];
				}
			} else {
				if (item.get(keyID) === currentID) {
					return this.get('stringFunction')(item);
				}
			}
		}
		return null;
	}),

	didInsertElement() {
		if (this.get('isFiltered') === true) {
			this.set('filterInput', this.$('input'));
		}
		this._super(...arguments);
	},

	filteredItems: Ember.computed('inputValue', 'items.[]', function() {
		var items = this.get('items'),
			inputValue = this.get('inputValue'),
			regex = new RegExp(inputValue, 'gi'),
			filterKeys = this.get('filterKeys');

		return this.get('isFiltered') === false ? items : items.filter(function(item) {
			for (var i = 0, l = filterKeys.length; i < l; i++) {
				if (regex.test(item.get(filterKeys[i])) === true) {
					return true;
				}
			}
			return false;
		});
	}),

	actions: {
		toggleDropdown() {
			this.get('dropdownService').toggleDropdown(this);
			if (this.get('isShowing') === true && this.get('isFiltered') === true) {
				this.get('filterInput').focus();
			}
		},
		escInput() {
			if (this.get('inputValue') === '') {
				this._actions['toggleDropdown'].apply(this);
				this.get('filterInput').blur();
			} else {
				this.set('inputValue', '');
			}
		},
	},
});
