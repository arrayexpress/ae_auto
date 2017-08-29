(function() {
    'use strict';
    // Should be in assets in non angular js code
    Object.prototype.getKeyByValue = function(value) {
        for (var prop in this) {
            if (this.hasOwnProperty(prop)) {
                if (this[prop] === value) {
                    return prop;
                }
            }
        }
    };

    var usersModule = angular.module('rootApp.users.services');

    usersModule.factory('Analysts', function($resource) {
        return $resource('/api/analysts/:id', {
            id: '@id'
        }, {
            'get': {
                method: 'GET',
                isArray: true
            },
            'put': {
                method: 'PUT',
            },
            'delete': {
                method: 'DELETE',
            }
        });
    });

    usersModule.factory('AnalystObj', function() {
        var apps = [],
            AVAILABLE_APPS = {
                'interactive': 'has_interactive_access',
                'live': 'has_live_access',
                'reporting': 'has_reporting_access',
                'streams': 'has_streams_access',
            };

        return {
            constructAnalystObject: function(analysts) {
                angular.forEach(analysts, function(analyst) {
                    analyst['selected'] = false;
                    for (var prop in AVAILABLE_APPS) {
                        if (analyst[AVAILABLE_APPS[prop]]) {
                            apps.push(AVAILABLE_APPS.getKeyByValue(AVAILABLE_APPS[prop]));
                        } else if (analyst['is_super_admin']) {
                            // We don't need to push the getKeyByValue in the apps array, because it results in
                            // undefined value in the apps array
                            if (prop !== 'getKeyByValue') {
                                apps.push(AVAILABLE_APPS.getKeyByValue(AVAILABLE_APPS[prop]));
                            }
                        }
                    }
                    analyst['apps'] = apps;
                    apps = [];
                    analyst.getType = function() {
                        var type = 'normal';
                        if (analyst['is_super_admin']) {
                            type = 'super admin';
                        } else if (analyst['is_admin']) {
                            type = 'admin';
                        }
                        return type;
                    };
                    analyst.getName = function() {
                        if (analyst['first_name'] || analyst['last_name']) {
                            return analyst['first_name'] + ' ' + analyst['last_name'];
                        }
                        return analyst['username'];
                    };
                });
                return analysts;
            }
        };
    });
})();
