(function() {
    'use strict';
    var usersModule = angular.module('rootApp.users.directives');

    usersModule.directive('userForm', function() {
        return {
            restrict: 'E',
            templateUrl: '/static/app/components/users/_registerForm.html',
            link: function(scope, element, attrs) {
                // Because of shared controller on different views,
                // we have to know which view are we on.
                scope.currentView(attrs.view);
            }
        };
    });
})();
