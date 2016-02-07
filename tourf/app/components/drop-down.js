import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'ul',
	classNames: ['dropdown'],
	classNameBindings: ['isShowing'],

	items: null,
	inputValue: '',
	isShowing: false,
	filterInput: null,
	isFiltered: false,
	filterKeys: null,
	currentID: null,
	keyID: 'id',

	currentItem: Ember.computed('currentID', 'items.[]', function() {
		var items = this.get('items'),
			currentID = this.get('currentID');
		for (var i = 0, l = items.get('length'); i < l; i++) {
			if (items.objectAt(i).get(this.get('keyID')) == currentID) {
				return this.get('stringFunction')(items.objectAt(i));
			}
		}
		return null;
	}),

	didInsertElement() {
		this.set('filterInput', this.$('input'));
		this._super(...arguments);
	},

	filteredItems: Ember.computed('inputValue', 'items.[]', function() {
		var items = this.get('items'),
			inputValue = this.get('inputValue'),
			regex = new RegExp(inputValue, 'gi'),
			filterKeys = this.get('filterKeys');

		return items.filter(function(item) {
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
			this.toggleProperty('isShowing');
			this.get('filterInput').focus();
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
