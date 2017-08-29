(function() {
    'use strict';
    var queriesModule = angular.module('rootApp.publications.directives');

    queriesModule.directive('publicationList', function() {
        return {
            restrict: 'E',
            scope: false,
            templateUrl: '/static/app/components/publications/_publicationListTmp.html'
        };
    });
})();
