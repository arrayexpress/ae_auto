(function() {
    'use strict';
    var rootAppServices = angular.module('rootApp.services');

    rootAppServices.factory('Errors', function() {
        return {
            addErrors: function(scope, errors) {
                scope.errors = {};
                for (var error in errors) {
                    scope.errors[error] = errors[error][0];
                }
            }
        };
    });
})();
