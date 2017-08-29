(function() {
    'use strict';
    var root = angular.module('rootApp');

    root.config(function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider,  cfpLoadingBarProvider) {
    //root.config(function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider,  cfpLoadingBarProvider) {
            // Turn off the loading bar spinner
            cfpLoadingBarProvider.includeSpinner = false;

            // Set Django CSRF token, for all XHR requests
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';


            // Translations
            //$translateProvider.useStaticFilesLoader({
            //    prefix: '/static/assets/json/locale-',
            //    suffix: '.json'
            //});

            //$translateProvider.useCookieStorage();
            //$translateProvider.preferredLanguage('en_US');

        })
        .run(function($rootScope, $state,  $uibModalStack, User, Permission, Flash) {
            $rootScope.flash = '';
            // Expose the translate service to the rootscope, to use it in all child scopes


            // Expose underscore library to the rootscope, to use it in all child scopes
            $rootScope._ = _;

            // Set has permission function globly so that all modules can use it
            // Will use ng if with has permission, because its more optimized that own hasPermission directive
            $rootScope.hasPermission = function(permission) {
                if (permission === 'all') {
                    return true;
                }
                return Permission.hasPermission(permission);
            };

            // Need to close the modal after changing routes from modal edit.
            $rootScope.$on('$stateChangeStart', function() {
                var top = $uibModalStack.getTop();
                if (top) {
                    $uibModalStack.dismiss(top.key);
                }
            });



            if (!$rootScope.user) {
                $rootScope.loading = true;
                var promise = User.get().$promise;

                promise.then(function(user) {
                    $rootScope.loading = false;
                    $rootScope.user = user;
                    Permission.setPermissions(user);
                    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
                        if (toState.data && toState.data.requiredPermission && !Permission.hasPermission(toState.data.requiredPermission)) {
                            event.preventDefault();
                            $state.go('index.dashboard');
                            return false;
                        }
                    });
                });

                promise.catch(function(resp) {
                    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
                        if (_.isEmpty($rootScope.user) && toState.name !== 'login' && toState.name !== 'register') {
                            event.preventDefault();
                            $state.go('login');
                            $rootScope.loading = false;
                            return false;
                        }

                    });
                    if (resp.status === 403 || resp.status === 401  && toState.name !== 'register') {
                        $state.go('login');
                        $rootScope.loading = false;
                    }
                });
            }
        });
})();
