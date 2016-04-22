"use strict";

var genApp = angular.module('GenApp', []);

genApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
});

genApp.controller('GenCtrl',
		['$scope', '$http',
		function($scope, $http) {

	$scope.isDisabled = true;
	$scope.hasRoundRobin = false;
	$scope.bracketType = 'single';
	$scope.bracketText = 'Single-elimination';
	$scope.useParticipants = true;
	$scope.numParticipants = 8;
	$scope.listInput = '';
	$scope.listItems = [];

	$scope.keydown = function(evt) {
		var keyCode = evt.keyCode || evt.which;
		if (keyCode === 27) {
			if ($scope.listInput) {
				$scope.listInput = null;
			} else {
				evt.target.blur();
			}
		} else if (keyCode === 13 && $scope.listInput) {
			$scope.listItems.push($scope.listInput);
			$scope.listInput = '';
			evt.target.focus();
			evt.preventDefault();
		}
	};

	$scope.removeItem = function($index) {
		$scope.listItems.splice($index, 1);
	};

	$scope.canSubmit = function() {
		if (['single', 'double'].indexOf($scope.bracketType) === -1) {
			return false;
		}
		if ($scope.hasRoundRobin === undefined) {
			return false;
		}
		if ($scope.useParticipants === undefined) {
			return false;
		}
		if ($scope.useParticipants === true && (angular.isArray($scope.listItems) === false || $scope.listItems.length < 1)) {
			return false;
		}
		if ($scope.useParticipants === false && (angular.isNumber($scope.numParticipants) === false || $scope.numParticipants < 1)) {
			return false;
		}
		return true;
	};

	var disabledCheck = function() {
		$scope.isDisabled = $scope.canSubmit() === true ? false : true;
	};

	$scope.$watchCollection('listItems', disabledCheck);
	$scope.$watchGroup(['hasRoundRobin', 'bracketType', 'useParticipants', 'numParticipants'], disabledCheck);

	$scope.generateBracket = function() {
		var params = {
			bracketType: $scope.bracketType,
			hasRoundRobin: $scope.hasRoundRobin,
			useParticipants: $scope.useParticipants,
		};

		if ($scope.useParticipants === false) {
			params.numParticipants = $scope.numParticipants;
		} else {
			params.listItems = $scope.listItems;
		}

		$http({
			method: 'GET',
			url: '/generator/json/',
			params: params,
		}).then(function successCallback(response) {
			// this callback will be called asynchronously
			// when the response is available
		}, function errorCallback(response) {
			// called asynchronously if an error occurs
			// or server returns response with an error status.
		});
	};

window.$scope = $scope;
}]);

genApp.constant('dropdownConfig', {
	keyedClass: 'keyed',
	openClass: 'is-showing',
	currentClass: 'current',
});

genApp.service('dropdownService', ['$document', '$rootScope', function($document, $rootScope) {
	var openScope = null;

	this.open = function(dropdownScope, element) {
		if (!openScope) {
			$document.on('click', closeDropdown);
			element.on('keydown', keybindFilter);
		}

		if (openScope && openScope !== dropdownScope) {
			openScope.isOpen = false;
		}

		openScope = dropdownScope;
	};

	this.close = function(dropdownScope, element) {
		if (openScope === dropdownScope) {
			openScope = null;
			$document.off('click', closeDropdown);
			element.off('keydown', keybindFilter);
		}
	};

	var closeDropdown = function(evt) {
		// This method may still be called during the same mouse event that
		// unbound this event handler. So check openScope before proceeding.
		if (!openScope) {
			return;
		}

		if (evt && evt.which === 3) {
			return;
		}

		var toggleElement = openScope.getToggleElement();
		if (evt && toggleElement && toggleElement[0].contains(evt.target) === true) {
			return;
		}

		if (evt) {
			for (var elems = openScope.getElems(), i = 0, l = elems.length; i < l; i++) {
				if (elems[i].node[0] === evt.target) {
					openScope.setSelectedOption(i);
					break;
				}
			}
		}

		openScope.isOpen = false;

		if (!$rootScope.$$phase) {
			openScope.$apply();
		}
	};

	var keybindFilter = function(evt) {
		if (evt.which === 27) {
			evt.stopPropagation();
			openScope.focusToggleElement();
			closeDropdown();
		} else if ([38, 40].indexOf(evt.which) !== -1 && openScope.isOpen) {
			evt.preventDefault();
			evt.stopPropagation();
			openScope.focusDropdownEntry(evt.which);
		} else if ([9, 13].indexOf(evt.which) !== -1 && openScope.isOpen) {
			var selectedOption = openScope.getSelectedOption(),
				fakeEvt = selectedOption !== false ? {target: selectedOption.node[0]} : undefined;
			evt.preventDefault();
			evt.stopPropagation();
			closeDropdown(fakeEvt);
		}
	};
}]);

genApp.controller('dropdownController',
		['$scope', '$attrs', '$animate', '$element', 'dropdownConfig', 'dropdownService',
		function($scope, $attrs, $animate, $element, dropdownConfig, dropdownService) {

	var self = this,
		scope = $scope.$new(), // create a child scope so we are not polluting original one
		getIsOpen,
		setIsOpen = angular.noop,
		elems = [],
		selectedOption = null;

	this.init = function() {
		if ($attrs.isOpen) {
			getIsOpen = $parse($attrs.isOpen);
			setIsOpen = getIsOpen.assign;

			scope.$watch(getIsOpen, function(value) {
				scope.isOpen = !!value;
			});
		}

		var items = $element[0].querySelectorAll('li[data-value]');
		for (var i = 0, l = items.length; i < l; i++) {
			elems[i] = {node: angular.element(items[i])};
			elems[i].text = elems[i].node.text();
			elems[i].value = elems[i].node[0].getAttribute('data-value');
		}
	};

	this.toggle = function(open) {
		scope.isOpen = arguments.length > 0 ? !!open : !scope.isOpen;

		if (angular.isFunction(setIsOpen) === true) {
			setIsOpen(scope, scope.isOpen);
		}

		return scope.isOpen;
	};

	scope.getElems = function() {
		return elems;
	};

	scope.getToggleElement = function() {
		return self.toggleElement;
	};

	scope.focusToggleElement = function() {
		if (self.toggleElement) {
			self.toggleElement[0].focus();
		}
	};

	scope.getSelectedOption = function() {
		return selectedOption !== null ? elems[selectedOption] : false;
	};

	scope.setSelectedOption = function(index) {
		for (var i = 0, l = elems.length; i < l; i++) {
			if (index === i) {
				selectedOption = index;
				elems[index].node.addClass(dropdownConfig.keyedClass);

				if ($scope.dropdownValue) {
					$scope.dropdownValue = elems[index].value;
				}
				if ($scope.dropdownText) {
					$scope.dropdownText = elems[index].text;
				}
			} else {
				elems[i].node.removeClass(dropdownConfig.keyedClass);
			}
		}
	};

	scope.focusDropdownEntry = function(keyCode) {
		switch (keyCode) {
			case 40: {
				if (angular.isNumber(selectedOption) === false) {
					selectedOption = 0;
				} else {
					selectedOption = selectedOption >= elems.length - 1 ? selectedOption : selectedOption + 1;
				}
				break;
			}
			case 38: {
				if (angular.isNumber(selectedOption) === false) {
					selectedOption = elems.length - 1;
				} else {
					selectedOption = selectedOption <= 0 ? 0 : selectedOption - 1;
				}
				break;
			}
		}

		for (var i = 0, l = elems.length; i < l; i++) {
			if (i === selectedOption) {
				elems[i].node.addClass(dropdownConfig.currentClass);
			} else if (elems[i].node.hasClass(dropdownConfig.currentClass) === true) {
				elems[i].node.removeClass(dropdownConfig.currentClass);
			}
		}
	};

	scope.$watch('isOpen', function(isOpen, wasOpen) {
		$animate[isOpen ? 'addClass' : 'removeClass']($element, dropdownConfig.openClass);

		if (isOpen) {
			scope.focusToggleElement();
			dropdownService.open(scope, $element);
		} else {
			dropdownService.close(scope, $element);
			selectedOption = null;

			for (var i = 0, l = elems.length; i < l; i++) {
				elems[i].node.removeClass(dropdownConfig.currentClass);
			}
		}

		if (angular.isFunction(setIsOpen) === true) {
			setIsOpen($scope, isOpen);
		}
	});
}]);

genApp.directive('dropdown', function() {
	return {
		restrict: 'A',
		scope: {
			dropdownText: "=",
			dropdownValue: '=',
		},
		controller: 'dropdownController',
		link: function(scope, element, attrs, dropdownCtrl) {
			dropdownCtrl.init();
		}
	};
});

genApp.directive('dropdownToggle', function() {
	return {
		restrict: 'A',
		require: '?^dropdown',
		link: function(scope, element, attrs, dropdownCtrl) {
			if (!dropdownCtrl) {
				return;
			}

			var openTimestamp = null;
			dropdownCtrl.toggleElement = element;

			var closeDropdown = function(evt) {
				evt.preventDefault();
				evt.stopPropagation();

				if (element.hasClass('disabled') === false && !attrs.disabled && Date.now() - openTimestamp > 200) {
					scope.$apply(function() {
						dropdownCtrl.toggle();
					});
				}
			};

			var openDropdown = function(evt) {
				evt.preventDefault();
				evt.stopPropagation();

				if (element.hasClass('disabled') === false && !attrs.disabled) {
					scope.$apply(function() {
						dropdownCtrl.toggle(true);
						openTimestamp = Date.now();
					});
				}
			};

			element.bind('click', closeDropdown);
			element.bind('focus', openDropdown);

			// WAI-ARIA
			element.attr({ 'aria-haspopup': true, 'aria-expanded': false });
			scope.$watch(dropdownCtrl.isOpen, function(isOpen) {
				element.attr('aria-expanded', !!isOpen);
			});

			scope.$on('$destroy', function() {
				element.unbind('click', closeDropdown);
			});
		}
	};
});
