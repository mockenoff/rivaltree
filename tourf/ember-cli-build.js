/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
	var app = new EmberApp(defaults, {
		replace: {
			files: [
				'index.html',
				'**/*.css',
				'**/*.js',
			],
			patterns: [],
			enabled: true,
		},
	});

	// Default to local/development settings
	var replacements = {
		assetsURL: '/static/assets',
		imagesURL: '/static/images',
	};

	// Replace options for production
	if(app.env === 'production') {
		app.options.minifyJS.enabled = true;
		app.options.minifyCSS.enabled = true;
	}

	// Build the replacement patterns
	for(var key in replacements) {
		app.options.replace.patterns.push({
			match: key,
			replacement: replacements[key],
		});
	}

	return app.toTree();
};
