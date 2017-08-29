(function() {
    'use strict';
    var usersModule = angular.module('rootApp.users.controllers');
    usersModule.controller('editAnalystController', function($scope, $uibModalInstance, $uibModal, $rootScope, Analysts, AnalystObj, Countries, Flash, analystClone, originalAnalyst, EditPassword, Errors) {
        $scope.errors = {};
        $scope.currentUserSettings = false;
        $scope.cancelResetBtn = 'cancel';

        $scope.currentView = function(view) {
            if (view === 'accountSettings') {
                $scope.cancelResetBtn = '';
                $scope.currentUserSettings = true;
            } else {
                $scope.cancelResetBtn = 'cancel';
                $scope.currentUserSettings = false;
            }

            if (analystClone.id === $rootScope.user.id) {
                console.log("value");
                $scope.currentUserSettings = true;
            }
        };
        var countriesPromise = Countries.get().$promise,
            managersPromise = Analysts.query({
                managers: '1'
            }).$promise;

        countriesPromise.then(function(countries) {
            $scope.countries = countries.list;
            if (_.isEmpty(analystClone)) {
                angular.copy($rootScope.user, analystClone);
                analystClone = AnalystObj.constructAnalystObject([analystClone])[0];
            }
            if (!_.isObject(analystClone.country)) {
                analystClone.country = {
                    name: analystClone.country
                };
            }
        });

        $scope.openEditPasswordModal = function() {
            $uibModal.open({
                templateUrl: '/static/app/components/users/_editPassword.html',
                controller: 'editAnalystController',
                size: 'lg',
                resolve: {
                    analystClone: function() {
                        return {};
                    },
                    originalAnalyst: function() {
                        return $rootScope.user;
                    }
                }
            });
        };

        managersPromise.then(function(managers) {
            $scope.managers = managers;
            $scope.analystForm.manager = _.findWhere(managers, {
                id: analystClone.manager
            });
        });

        $scope.analystForm = analystClone;


        $scope.reset = function() {
            $uibModalInstance.close('close');
        };

        $scope.savePassword = function() {
            if ($scope.editForm.password !== $scope.editForm.confirmPassword) {
                Errors.addErrors($scope, {
                    confirmPassword: ['password didn"t match']
                });
                return;
            }
            EditPassword.edit(originalAnalyst.id, $scope.editForm.password)
                .success(function() {
                    $uibModalInstance.close();
                    Flash.show('password successfully edited.', 'success', 3000);
                })
                .error(function(error) {
                    Errors.addErrors($scope, error);
                    Flash.show('something went wrong.', 'error', 3000);
                });
        };

        $scope.save = function() {
            var country = $scope.analystForm.country,
                params = {};
            angular.copy(analystClone, params);

            // Hack-ish but required, because the country list json is an object,
            // and the return value from the server is a string.
            if (_.isObject(country)) {
                params.country = country.name;
            }

            if ($scope.analystForm.manager) {
                params.manager = $scope.analystForm.manager.id;
            }

            var promise = Analysts.put({
                id: analystClone.id
            }, params).$promise;

            promise.then(function(editedAnalyst) {
                // Reconstruct the analyst object for new permissions
                // Have to send it an array because the function expect an array
                var editedAnalystObject = AnalystObj.constructAnalystObject([$scope.analystForm]);

                // Check if the edited user is the logged in user, then we change the logged in user as well,
                // and if the view is opened from the account settings page then also we change the logged in user
                if (originalAnalyst.id === $rootScope.user.id || _.isEmpty($uibModalInstance)) {
                    $rootScope.user = originalAnalyst;
                }

                // Replace the original Analyst  by the edited analyst
                // construct function returns an array so we take the 1st element only,
                // which is the edited analyst
                angular.copy(editedAnalystObject[0], originalAnalyst);

                // if the view is opened from modal , then close the modal
                if (!_.isEmpty($uibModalInstance)) {
                    $uibModalInstance.close();
                }

                Flash.show('user successfully edited.', 'success', 3000);
            });

            promise.catch(function(response) {
                Errors.addErrors($scope, response.data);
            });

        };
    });
})();
