(function() {
    'use strict';
    var navModule = angular.module('rootApp.nav.controllers');

    navModule.controller('applicationNavController', function($scope, $rootScope, $location) {
        $scope.apps = [
        //    {
        //    name: 'dashboard',
        //    route: 'dashboard',
        //    icon: 'dashboard',
        //    permission: 'all'
        //},
            {
            name: 'Publications',
            route: 'publications',
            icon: 'align-justify',
            permission: 'all'
        }, {
            name: 'reporting',
            route: 'reporting',
            icon: 'file-pdf-o',
            permission: 'reporting'
        }, {
            name: 'interactive',
            route: 'interactive',
            icon: 'bar-chart',
            permission: 'interactive'
        }, {
            name: 'streams',
            route: 'streams',
            icon: 'line-chart',
            permission: 'streams'
        }, {
            name: 'live',
            route: 'live',
            icon: 'clock-o',
            permission: 'live'
        }, {
            name: 'add query',
            route: 'addQuery',
            icon: 'plus',
            permission: 'admin'
        }, {
            name: 'add analyst',
            route: 'addAnalyst',
            icon: 'plus-square',
            permission: 'admin'
        }];
    });

})();
