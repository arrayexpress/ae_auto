(function() {
    'use strict';
    var directives = angular.module('rootApp.directives');

    directives.directive('hasPermission', function(Permission) {
        return {
            link: function(scope, element, attrs) {
                var value = attrs.hasPermission.trim();
                var notPermissionFlag = value[0] === '!';
                if (notPermissionFlag) {
                    value = value.slice(1).trim();
                }

                var toggleVisibilityBasedOnPermission = function() {
                    var hasPermission = Permission.hasPermission(value);

                    if (hasPermission !== notPermissionFlag || hasPermission !== notPermissionFlag) {
                        element.removeClass('hidden');
                    } else {
                        element.addClass('hidden');
                    }
                };
                toggleVisibilityBasedOnPermission();
                scope.$on('permissionsChanged', toggleVisibilityBasedOnPermission);
            }
        };
    });
})();
