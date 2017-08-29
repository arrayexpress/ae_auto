(function() {
    'use strict';
    var usersModule = angular.module('rootApp.users.controllers');
    usersModule.controller('addUsersController', function($scope, $rootScope, Countries, $state, Register, Flash, Errors, Auth, Permission) {

        // Just a placeholder, because it has no use here, but used in edit views
        $scope.currentView = function(view) {
            return;
        };

        $scope.newUser = true;
        $scope.cancelResetBtn = 'reset';

        $scope.analystForm = {

        };





        $scope.save = function() {
            if ($scope.analystForm.password !== $scope.analystForm.confirmPassword) {
                Errors.addErrors($scope, {
                    confirmPassword: ['password didn"t match']
                });
                return;
            }


            var promise = Register.reg($scope.analystForm);


            promise.success(function(resp) {
                Flash.show('user created successfully.', 'success', 3000);
                 $scope.user = {
                     'username': $scope.analystForm.username,
                     'password': $scope.analystForm.password
                 };
                var promise = Auth.auth($scope.user);
                promise.success(function(user) {
                    $rootScope.user = user;
                    Permission.setPermissions(user);
                    $state.go('index.publications');
                });
            });

            promise.error(function(errors) {
                Errors.addErrors($scope, errors);
            });

        };
        $scope.reset = function() {
            for (var prop in $scope.analystForm) {
                if ($scope.analystForm.hasOwnProperty(prop)) {
                    $scope.analystForm[prop] = '';
                }
            }
        };
    });
})();
