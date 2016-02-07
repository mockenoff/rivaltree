/* jshint node: true */

module.exports = function(environment) {
	var ENV = {
		modulePrefix: 'tourf',
		podModulePrefix: 'tourf/pods',
		environment: environment,
		baseURL: '/dash/',
		rootURL: '/',
		apiURL: '/api',
		locationType: 'auto',
		EmberENV: {
			FEATURES: {
				// Here you can enable experimental features on an ember canary build
				// e.g. 'with-controller': true
			}
		},

		APP: {
			// Here you can pass flags/options to your application instance
			// when it is created
		},

		contentSecurityPolicy: {
			'default-src': "'none'",
			'script-src': "'self'",
			'font-src': "'self' fonts.gstatic.com",
			'connect-src': "'self'",
			'img-src': "'self' data:",
			'media-src': "'self'",
		},
	};

	if (environment === 'development') {
		// ENV.APP.LOG_RESOLVER = true;
		// ENV.APP.LOG_ACTIVE_GENERATION = true;
		// ENV.APP.LOG_TRANSITIONS = true;
		// ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
		// ENV.APP.LOG_VIEW_LOOKUPS = true;
		ENV.apiURL = 'http://local.rivaltree.com:8000/api';
		ENV.contentSecurityPolicy['script-src'] = "'self' local.rivaltree.com:49152"
		ENV.contentSecurityPolicy['connect-src'] = "'self' localhost:8000 local.rivaltree.com:8000 ws://local.rivaltree.com:49152"
	}

	if (environment === 'test') {
		// Testem prefers this...
		ENV.baseURL = '/';
		ENV.locationType = 'none';

		// keep test console output quieter
		ENV.APP.LOG_ACTIVE_GENERATION = false;
		ENV.APP.LOG_VIEW_LOOKUPS = false;

		ENV.APP.rootElement = '#ember-testing';
	}

	if (environment === 'production') {
		// Nothing?
	}

	return ENV;
};
