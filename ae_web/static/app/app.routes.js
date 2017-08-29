(function() {
    'use strict';
    var root = angular.module('rootApp');

    root.config(function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        // Set root route to index, if no other routes exist
        $urlRouterProvider.otherwise('dashboard');

        // Set the default empty route to dashboard
        $urlRouterProvider.when('', 'publications');
        //$urlRouterProvider.when('', 'springframework');


        $stateProvider
            .state('index', {
                url: '',
                abstract: true,
                views: {
                    'header': {
                        templateUrl: '/static/app/components/core/header/_header.html',
                        controller: 'headerController'
                    },
                    'applicationNav': {
                        templateUrl: '/static/app/components/core/applicationNav/_nav.html',
                        controller: 'applicationNavController'
                    },
                    'footer': {
                        templateUrl: '/static/app/components/core/footer/_footer.html',
                    },
                }
            })
           .state('login', {
                'url': '/login',
                views: {
                    'content': {
                        templateUrl: '/static/app/components/login/_login.html',
                        controller: 'loginController'
                    },
                    'footer': {
                        templateUrl: '/static/app/components/core/footer/_footer.html',
                    },
                },
            }).state('register', {
                'url': '/register',
                views: {
                    'content': {
                        templateUrl: '/static/app/components/users/_register.html',
                        controller: 'addUsersController'
                    },
                    'footer': {
                        templateUrl: '/static/app/components/core/footer/_footer.html',
                    },
                },
            }).state('index.dashboard', {
                'url': '/dashboard',
                views: {
                    'content@': {
                        templateUrl: '/static/app/components/dashboard/_dashboard.html',
                        controller: 'dashboardController'
                    }
                },
            }).state('index.publications', {
                'url': '/publications',
                views: {
                    'content@': {
                        templateUrl: '/static/app/components/publications/_publications.html',
                        controller: 'publicationsController'
                    }
                },
            });
    });

})();
