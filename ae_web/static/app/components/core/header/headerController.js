(function() {
    'use strict';
    var headerModule = angular.module('rootApp.header.controllers');
    headerModule.controller('headerController', function($scope, SpringFramework) {

        $scope.restart_framework = function(){
           console.log('restart');
            var frameworkPromise = SpringFramework.post().$promise;
            frameworkPromise.then(function(response){
                var springframework = response.results;
                //console.log(response);
                //console.log(springframework);
                //console.log('Success')
            })
        };
        $scope.navs = [
        //    {
        //    name: 'settings',
        //    link: 'settings',
        //    permission: 'all'
        //}, {
        //    name: 'all analysts',
        //    link: 'allAnalysts',
        //    permission: 'admin'
        //}, {
        //    name: 'dictionaries',
        //    link: 'dicts',
        //    permission: 'all'
        //}
        ];
    });
})();
