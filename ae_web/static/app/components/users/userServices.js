(function() {
    'use strict';
    var usersModule = angular.module('rootApp.users.services');

    usersModule.factory('User', function($resource) {
        return $resource('/api/me', {}, {
            'get': {
                method: 'GET',
                ignoreLoadingBar: true
            }
        });
    });

    usersModule.factory('Countries', function($resource) {
        return $resource('/static/assets/json/countryList.json', {}, {
            'get': {
                method: 'GET',
            }
        });
    });


    usersModule.factory('EditPassword', function($http) {
        return {
            edit: function(userId, password) {
                return $http({
                    method: 'POST',
                    url: '/accounts/edit',
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
                    data: {
                        password: password,
                        id: userId
                    }
                });
            }
        };
    });

    usersModule.factory('Register', function($http) {
        return {
            reg: function(user) {
                return $http({
                    method: 'POST',
                    url: '/accounts/register',
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
