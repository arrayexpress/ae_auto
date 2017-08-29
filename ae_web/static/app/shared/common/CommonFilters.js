(function() {
    'use strict';
    var rootAppFilters = angular.module('rootApp.filters');

    rootAppFilters.filter('cut', function() {
        return function(value, wordwise, max, tail) {
            if (!value) {
                return '';
            }

            max = parseInt(max, 10);
            if (!max) {
                return value;
            }
            if (value.length <= max) {
                return value;
            }

            value = value.substr(0, max);
            if (wordwise) {
                var lastspace = value.lastIndexOf(' ');
                if (lastspace !== -1) {
                    value = value.substr(0, lastspace);
                }
            }

            return value + (tail || ' …');
        };
    });

    rootAppFilters.filter('cleanError', function() {
        return function(value) {
            if (value) {
                return value.replace('.', ' ').toLowerCase();
            }
        };
    });
})();
