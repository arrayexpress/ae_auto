(function() {
    'use strict';
    var root = angular.module('rootApp', [
        'rootApp.services',
        'rootApp.directives',
        'rootApp.filters',
        'rootApp.controllers',
        'rootApp.login.controllers',
        'rootApp.login.services',
        'rootApp.header.services',
        'rootApp.header.controllers',
        'rootApp.nav.controllers',
        'rootApp.users.controllers',
        'rootApp.users.services',
        'rootApp.users.directives',
        //'rootApp.settings.controllers',
        //'rootApp.settings.services',
        //'rootApp.dashboard.controllers',
        //'rootApp.dashboard.services',
        //'rootApp.dicts.controllers',
        //'rootApp.dicts.services',
        'rootApp.publications.controllers',
        'rootApp.publications.services',
        'rootApp.publications.directives',
        //'rootApp.reports.controllers',
        //'rootApp.reports.services',
        'ngAnimate', /* because bootstrap */
        'ui.bootstrap.tpls',
        'ui.bootstrap',
        'ngResource',
        'ui.router',
        'ngCookies',
        'pascalprecht.translate',
        //'nvd3',
        'colorpicker.module',
        'angular-loading-bar',
        //'angularMoment',
    ]);

    angular.module('rootApp.services', []);
    angular.module('rootApp.directives', []);
    angular.module('rootApp.filters', []);
    angular.module('rootApp.controllers', []);
    // Login module definitions
    angular.module('rootApp.login.controllers', []);
    angular.module('rootApp.login.services', []);

    // Header module definitions
    angular.module('rootApp.header.controllers', []);
    angular.module('rootApp.header.services', []);

    // Navigation module definitions
    angular.module('rootApp.nav.controllers', []);

    // Settings module definitions
    //angular.module('rootApp.settings.controllers', []);
    //angular.module('rootApp.settings.services', []);

    // User module definitions
    angular.module('rootApp.users.controllers', []);
    angular.module('rootApp.users.services', []);
    angular.module('rootApp.users.directives', []);
    //
    //
    //// Dashboard module definitions
    //angular.module('rootApp.dashboard.controllers', []);
    //angular.module('rootApp.dashboard.services', []);
    //
    //// Dictionaries module definitions
    //angular.module('rootApp.dicts.controllers', []);
    //angular.module('rootApp.dicts.services', []);
    //
    // Publication module definitions
    angular.module('rootApp.publications.controllers', []);
    angular.module('rootApp.publications.services', []);
    angular.module('rootApp.publications.directives', []);
    //// Reports module definitions
    //angular.module('rootApp.reports.controllers', []);
    //angular.module('rootApp.reports.services', []);

})();
