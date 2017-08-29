(function() {
    'use strict';
    var queryModule = angular.module('rootApp.queries.controllers');

    queryModule.controller('editQueryController', function($scope, $rootScope, $uibModalInstance, Publications, QueryObj, Channels, ChannelTypes, ChannelTypesObj, Dictionaries, IconsObj, Flash, queryClone, originalQuery, Analysts) {
        $scope.smChannelName = ChannelTypesObj.getNetworkById(queryClone['sm_channel'].type).displayName;

        var query = $scope.query = queryClone;

        // NOT DRY, needs to check this later.
        var allUsersPromise = Analysts.get().$promise,
            allDictsPromise = Dictionaries.get().$promise;

        allUsersPromise.then(function(users) {
            users.forEach(function(user) {
                user['selected'] = false;
            });
            $scope.userResults = users;
            query.users.forEach(function(userId) {
                _.findWhere($scope.userResults, {
                    id: userId
                }).selected = true;
            });
        });

        allDictsPromise.then(function(dicts) {
            dicts.forEach(function(item) {
                dicts['selected'] = false;
            });

            console.log(query);
            query.dictionaries.forEach(function(dict) {
                _.findWhere(dicts, {
                    'name': dict.name
                }).selected = true;
            });

            $scope.dictionaryResults = dicts;
        });

        $scope.applicationResults = [{
            'application': 'interactive',
            'selected': false
        }, {
            'application': 'reporting',
            'selected': false
        }, {
            'application': 'live',
            'selected': false
        }, {
            'application': 'streams',
            'selected': false
        }];

        $scope.applicationResults.forEach(function(application) {
            if (query[application.application]) {
                application.selected = true;
            }
        });

        $scope.selectDictionary = function(index) {
            $scope.dictionaryResults[index]['selected'] = !$scope.dictionaryResults[index]['selected'];
        };

        $scope.selectUser = function(index) {
            $scope.userResults[index]['selected'] = !$scope.userResults[index]['selected'];
        };

        $scope.selectApplication = function(index) {
            $scope.applicationResults[index]['selected'] = !$scope.applicationResults[index]['selected'];
        };

        $scope.cancel = function() {
            $uibModalInstance.close();
        };

        $scope.save = function() {
            var form = {},
                channelForm = {};

            angular.copy(query, form);

            var channelName = ChannelTypesObj.getNetworkById(form['sm_channel'].type).displayName;

            channelForm = {
                type: form['sm_channel'].type,
                identifier: form['sm_channel'].identifier
            };

            var channelPromise = Channels.put({
                id: form['sm_channel'].id
            }, channelForm).$promise;

            channelPromise.then(function(channel) {
                var selectedUsers = _.where($scope.userResults, {
                        selected: true
                    }),
                    selectedDicts = _.where($scope.dictionaryResults, {
                        selected: true
                    }),
                    selectedApps = _.where($scope.applicationResults, {
                        selected: true
                    });

                form.users = [];
                angular.forEach(selectedUsers, function(user) {
                    form.users.push(user.id);
                });
                form.users.push($rootScope.user.id);

                form.dictionaries = [];
                angular.forEach(selectedDicts, function(dict) {
                    form.dictionaries.push(dict.id);
                });

                $scope.applicationResults.forEach(function(applications) {
                    form[applications['application']] = false;
                });
                angular.forEach(selectedApps, function(app) {
                    form[app['application']] = true;

                });

                form['sm_channel'] = channel.id;
                var queryPromise = Queries.put({
                    id: query.id
                }, form).$promise;

                queryPromise.then(function(editedQuery) {
                    var queryObj = QueryObj.constructQueryObject([editedQuery]),
                        queryDicts = queryObj[0]['dictionaries'];
                    queryObj[0]['sm_channel'] = channel;
                    queryObj[0]['dictionaries'] = [];
                    queryDicts.forEach(function(dictId) {
                        console.log(dictId);
                        console.log($scope.dictionaryResults);
                        queryObj[0]['dictionaries'].push(_.findWhere($scope.dictionaryResults, {
                            id: dictId
                        }));
                    });
                    angular.copy(queryObj[0], originalQuery);
                    $uibModalInstance.close();
                    Flash.show('query edited successfully');
                });
            });
        };
    });
})();
