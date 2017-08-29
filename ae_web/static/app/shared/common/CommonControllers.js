(function() {
    'use strict';
    var rootAppControllers = angular.module('rootApp.controllers');

    rootAppControllers.controller('confirmModalController', function($scope, $rootScope, $modalInstance, type) {
        $scope.confirm = function() {
            $rootScope.$emit('destroy' + type);
            $modalInstance.close();
        };

        $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
        };

    });

})();
