(function() {
    'use strict';
    var queryModule = angular.module('rootApp.queries.controllers');
    queryModule.controller('viewQueryController', function($scope, $rootScope, $stateParams) {
        $scope.queryId = $stateParams.id;
        $scope.since = '';
        $scope.until = '';
        $scope.sentiment = '';
        $scope.entities = '';
        $scope.topics = '';
        $scope.flag = false;
        $scope.generateUrls = function() {
            $scope.flag = true;

            var param = [];

            var d = null;

            if ($scope.since && $scope.since !== 0) {
                d = new Date($scope.since);
                var sinceTs = (d.getTime() / 1000) - (d.getTimezoneOffset() * 60);
                param.push('since=' + sinceTs);
            }
            if ($scope.until && $scope.until !== 0) {
                d = new Date($scope.until);
                var untilTs = (d.getTime() / 1000) - (d.getTimezoneOffset() * 60);
                console.log(untilTs);
                param.push('until=' + untilTs);
            }
            $scope.interactionsParams = param.join('&');

            if ($scope.sentiment) {
                param.push('sentiment=' + $scope.sentiment);
            }
            if ($scope.entities) {
                param.push('entities=' + $scope.entities);
            }
            if ($scope.topics) {
                param.push('topics=' + $scope.topics);
            }
            $scope.statsParams = param.join('&');
        };
    });
})();
