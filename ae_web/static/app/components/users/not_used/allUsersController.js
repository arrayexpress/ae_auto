(function() {
    'use strict';
    var usersModule = angular.module('rootApp.users.controllers');
    usersModule.controller('allUsersController', function($scope, $rootScope, $uibModal, Analysts, AnalystObj, Flash) {
        var promise = Analysts.get().$promise;


        promise.then(function(analysts) {
            $scope.analysts = AnalystObj.constructAnalystObject(analysts);
        });

        $scope.deleteAnalyst = function(analyst) {
            $uibModal.open({
                templateUrl: '/static/app/shared/common/_confirmModal.html',
                controller: 'confirmModalController',
                size: 'sm',
                resolve: {
                    type: function() {
                        return 'User';
                    }
                }
            });
            // The $on function returns a listerer destroyer so we need to catch it in a variable,
            // to call it after the delete promise is done
            // so it doesnt conflict with other destroy events on different controllers
            var removeListener = $rootScope.$on('destroyUser', function() {

                var promise = Analysts.delete({
                    id: analyst.id
                }).$promise;

                promise.then(function() {
                    $scope.analysts.splice($scope.analysts.indexOf(analyst), 1);

                    Flash.show('User successfully deleted.', 'success');

                    removeListener();
                });
                promise.catch(function(response) {
                    Flash.show(response.data.error, 'error');

                    removeListener();
                });
            });
        };

        $scope.openEditModal = function(analyst) {
            var analystClone = {};
            // Need to deep copy the analyst,
            // because it will edit the existent copy of it in the HTML table.
            angular.copy(analyst, analystClone);
            $uibModal.open({
                templateUrl: '/static/app/components/users/_editAnalyst.html',
                controller: 'editAnalystController',
                size: 'lg',
                resolve: {
                    analystClone: function() {
                        return analystClone;
                    },
                    originalAnalyst: function() {
                        return analyst;
                    }
                }
            });
        };

        $scope.openEditPasswordModal = function(analyst) {
            $uibModal.open({
                templateUrl: '/static/app/components/users/_editPassword.html',
                controller: 'editAnalystController',
                size: 'lg',
                resolve: {
                    analystClone: function() {
                        return {};
                    },
                    originalAnalyst: function() {
                        return analyst;
                    }
                }
            });
        };
    });
})();
