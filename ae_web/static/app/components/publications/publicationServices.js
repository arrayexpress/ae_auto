(function() {
    'use strict';
    var publicationModule = angular.module('rootApp.publications.services');
    publicationModule.factory('SpringFramework',['$resource', function($resource) {
        return $resource('/api/maintenance/framework/restart', {}, {
             'post': {
                method: 'POST'
            }
        }


        );
    }]);
    publicationModule.factory('Publications', function($resource) {
        return $resource('/api/publications/:id', {
            id: '@id'
        }, {
            'get': {
                method: 'GET',
            },
            'put': {
                method: 'PUT',
            },
            'post': {
                method: 'POST',
            },
            'delete': {
                method: 'DELETE',
            }
        });

    });

    publicationModule.factory('EditPublicationStatus', function($http) {
        return {
            edit: function(association_id, status) {
                return $http({
                    method: 'POST',
                    url: '/api/publications/edit',
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
                        status: status,
                        id: association_id
                    }
                });
            }
        };
    });

})();
