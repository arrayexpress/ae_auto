(function() {
    'use strict';
    var root = angular.module('rootApp.services');


    root.factory('Flash', function($rootScope, $timeout) {
        return {
            show: function(message, type, millis) {
                type = type || 'success';
                $rootScope[type] = true;
                millis = millis || 2000;
                $rootScope.flash = message;
                $timeout(function() {
                    $rootScope.flash = '';
                    $rootScope['success'] = true;
                    $rootScope['error'] = false;
                }, millis);
            }
        };
    });
})();
