(function() {
    'use strict';
    var loginModule = angular.module('rootApp.login.services');

    loginModule.factory('Auth', function($http) {
        return {
            auth: function(user) {
                return $http({
                    method: 'POST',
                    url: '/accounts/login',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    transformRequest: function(obj) {
                        var str = [];
                        for (var p in obj) {
                            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                        }
                        return str.join("&");
                    },
                    data: user
                });
            }
        };
    });
})();
