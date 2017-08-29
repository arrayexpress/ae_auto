(function() {
    'use strict';
    var loginModule = angular.module('rootApp.login.controllers');

    loginModule.controller('loginController', function($scope, $rootScope, $state,  Auth, Flash, Permission) {

        $scope.user = {
            'username': '',
            'password': ''
        };


        $scope.login = function() {
            var promise = Auth.auth($scope.user);

            promise.success(function(user) {
                $rootScope.user = user;
                Permission.setPermissions(user);
                $state.go('index.publications');
            });

            promise.error(function(resp) {
                $scope.validationError = true;
                Flash.show(resp.error, 'error', 3000);
            });
        };
    });
})();
