(function() {
    'use strict';
    var root = angular.module('rootApp.services');

    root.factory('Permission', function($rootScope) {
        var permissionList = ['all'],
            AVAILABLE_PERMISSIONS = {
                'admin': 'is_admin',
                'superAdmin': 'is_super_admin'
            };
        return {
            setPermissions: function(user) {
                for (var prop in AVAILABLE_PERMISSIONS) {
                    if (user[AVAILABLE_PERMISSIONS[prop]] || user['is_super_admin']) {
                        if (prop === 'getKeyByValue') {
                            continue;
                        }
                        permissionList.push(prop);
                    }
                }
                $rootScope.$broadcast('permissionsChanged');
            },
            getPermissions: function() {
                return permissionList;
            },
            hasPermission: function(permission) {
                return _.indexOf(permissionList, permission) !== -1;
            },
            clearPermissions: function() {
                permissionList = ['all'];
                return permissionList;
            }
        };
    });
})();
