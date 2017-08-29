(function() {
    'use strict';
    var queryModule = angular.module('rootApp.queries.controllers');
    queryModule.controller('addQueryController', function($scope, $rootScope, $timeout, $state, $uibModalInstance, Publications, QueryObj, Channels, ChannelTypes, ChannelTypesObj, GetUserApps, Dictionaries, DictObj, TwitterSearch, FacebookSearch, InstagramSearch, YoutubeSearch, Analysts, AnalystObj, Flash, Tokens, FbGroups, Errors, queryClone, originalQuery) {

        /**************************** Add Query view ************************/
        $scope.currentStep = 'query type';

        $scope.validQuery = false;
        $scope.step = [];

        $scope.queryForm = {
            smChannel: false,
            name: '',
            users: [],
            dictionaries: [],
            'sm_channel': '',
            live: false,
            streams: false,
            interactive: false,
            reporting: false,
            searchName: '',
            query: ''
        };

        var tokenPromise = Tokens.get().$promise;

        tokenPromise.then(function(tokens) {
            $scope.tokens = tokens;
        });

        var smChannelsPromise = ChannelTypes.get().$promise;
        smChannelsPromise.then(function(types) {
            $scope.smChannels = ChannelTypesObj.constructObj(types, true);
        });

        $scope.queryName = {
            query: ''
        };
        $scope.twitterResults = {};
        $scope.facebookResults = {};
        $scope.queryForm.name = '';

        $scope.currentPage = 1;

        $scope.paginate = function(value) {
            $scope.currentPage += value;
            $scope.selected = -1;
            $scope.searchQueryName();
        };

        $scope.searchQueryName = function() {
            // Clear selectedQuery and queryForm.query, Because we don't want it to select the previous query
            // when we search for another query
            $scope.selectedQuery = {};
            $scope.queryForm.query = {};

            // Empty search results after another search
            $scope.searchResults = [];
            switch ($scope.queryForm.smChannel.displayName) {
                case 'twitter account':
                    {
                        var twitterPromise = TwitterSearch.get({
                            'query': $scope.queryForm.searchText,
                            'page': $scope.currentPage
                        }).$promise;
                        twitterPromise.then(function(response) {
                            $scope.searchResults = response;
                        });
                        break;
                    }
                case 'facebook page':
                    {
                        var facebookPromise = FacebookSearch.get({
                            'query': $scope.queryForm.searchText
                        }).$promise;
                        facebookPromise.then(function(response) {
                            $scope.searchResults = response.data;
                        });
                        break;
                    }
                case 'instagram account':
                    {
                        var instagramPromise = InstagramSearch.get({
                            'query': $scope.queryForm.searchText
                        }).$promise;
                        instagramPromise.then(function(response) {
                            $scope.searchResults = response;
                        });
                        break;
                    }
                case 'youtube channel':
                    {
                        var YoutubePromise = YoutubeSearch.get({
                            'query': $scope.queryForm.searchText
                        }).$promise;
                        YoutubePromise.then(function(response) {
                            $scope.searchResults = response;
                        });
                        break;
                    }

            }
        };

        $scope.streamResults = [{
            'name': 'public',
            'selected': true,
            'id': 1
        }, {
            'name': 'gnip',
            'selected': false,
            'id': 2
        }];

        var allDictsPromise = Dictionaries.get().$promise;
        allDictsPromise.then(function(dicts) {
            $scope.dictionaryResults = DictObj.constructDictObject(dicts);

            // We have to put this here so we can get selected dicts for the edit view
            if (!_.isEmpty(queryClone)) {
                query.dictionaries.forEach(function(dict) {
                    $scope.selectDictionary(dict);
                });
            }

        });

        if ($rootScope.user) {
            // Prepare logged in user, to get his apps , so we can view them , instead of
            // viewing all the apps.
            var loggedInUser = AnalystObj.constructAnalystObject([$rootScope.user])[0];
            $scope.applicationResults = GetUserApps.constructObj(loggedInUser.apps);
        }

        var allUsersPromise = Analysts.get().$promise;
        allUsersPromise.then(function(users) {
            $scope.userResults = AnalystObj.constructAnalystObject(users);

            // We have to put this here so we can get selected analysts for the edit view
            if (!_.isEmpty(queryClone)) {
                query.users.forEach(function(userId) {
                    var user = _.findWhere($scope.userResults, {
                        id: userId
                    });
                    $scope.selectItem(user, $scope.userResults);
                });
            }
        });

        $scope.toggleValidQuery = function() {
            $scope.validQuery = false;
            $scope.editValidQuery = true;
        };

        $scope.checkQuery = function() {
            var queryString = '';
            if ($scope.queryForm.query) {
                queryString = $scope.queryForm.query;

            } else if ($scope.query) {
                queryString = $scope.query['sm_channel'].identifier;
            }

            var finalString = '';
            var regExp = /[()]/gi;
            queryString = queryString.replace(regExp, '');
            if (queryString.indexOf(' OR ') === -1 && queryString.indexOf(' AND ') === -1) {
                $scope.validQuery = true;
                return;
            }

            var stringArr = [];

            queryString = queryString.split(' OR ');
            if (queryString.length === 1) {
                finalString = '( ' + queryString.join(' AND ') + ' )';
                if ($scope.queryForm.query) {
                    $scope.queryForm.query = finalString;
                } else {
                    $scope.query['sm_channel'].identifier = finalString;
                }
                $scope.validQuery = true;
                $scope.editValidQuery = false;
                return;
            }

            queryString.forEach(function(str) {
                if (str.indexOf(' AND ') > -1) {
                    stringArr.push('( ' + str + ' )');
                } else {
                    stringArr.push(str);
                }


            });
            finalString = '( ' + stringArr.join(' OR ') + ' )';

            if ($scope.queryForm.query) {
                $scope.queryForm.query = finalString;
            } else {
                $scope.query['sm_channel'].identifier = finalString;
            }
            $scope.validQuery = true;
            $scope.editValidQuery = false;
        };
        $scope.addLogicalOpertor = function(opertor) {
            if ($scope.queryForm.smChannel || $scope.queryForm['sm_channel']) {
                $scope.queryForm.query += ' ' + opertor + ' ';
                $scope.focusInput = true;
            }

            if ($scope.query) {
                $scope.query['sm_channel'].identifier += ' ' + opertor + ' ';
                $scope.focusInput = true;
            }
            // Little hack to retrigger the input focus,
            // becuase the directive needs a non 0 time to set the focus back,
            // So we have to give a non 0 time to set it back to false again.
            $timeout(function() {
                $scope.focusInput = false;
            });
        };

        $scope.changeStep = function(step) {
            // Empty search results after changing step
            $scope.searchResults = [];
            $scope.queryForm.searchText = '';
            $scope.validQuery = false;
            if (step === 1) {
                $scope.currentStep = $scope.queryForm.smChannel.displayName;
            } else if (step === 2) {
                if (typeof $scope.queryForm.query === 'object') {
                    if ($scope.queryForm.smChannel.channel === 'instagram') {
                        $scope.currentStep = $scope.queryForm.query['full_name'];
                    } else if ($scope.queryForm.smChannel.channel === 'youtube') {
                        $scope.currentStep = $scope.queryForm.query['snippet']['title'];
                    } else {
                        $scope.currentStep = $scope.queryForm.query.name;
                    }

                } else {
                    $scope.currentStep = $scope.queryForm.query;
                }
            } else {
                $scope.currentStep = 'query type';
            }

            $scope.step[step] = {};
            $scope.step[step].active = true;
        };

        $scope.selectQuery = function(result) {
            $scope.selectedQuery = result;
            $scope.queryForm.query = result;
        };
        $scope.selectStream = function(result) {
            var stream = _.findWhere($scope.streamResults, {
                name: result.name
            });
            var streamSelected = _.findWhere($scope.streamResults, {
                selected: true
            });
            if (streamSelected) {
                streamSelected.selected = false;
            }
            stream.selected = !stream.selected;

            // $scope.selectedDict = result;
        };
        $scope.selectDictionary = function(result) {
            var dict = _.findWhere($scope.dictionaryResults, {
                id: result.id
            });
            dict.selected = !dict.selected;
            var defaultEng = _.findWhere($scope.dictionaryResults, {
                name: 'default english'
            });
            var defaultArabic = _.findWhere($scope.dictionaryResults, {
                name: 'default arabic'
            });
            if (dict.name === 'default arabic') {
                defaultEng.selected = false;
            }
            if (dict.name === 'default english') {
                defaultArabic.selected = false;
            }

            // $scope.selectedDict = result;
        };
        $scope.selectItem = function(result, arr) {
            var selectedItem = _.findWhere(arr, {
                id: result.id
            });
            selectedItem.selected = !selectedItem.selected;
        };
        $scope.selectItems = function(arr) {
            //arr.forEach(function () {

            //});
            //var selectedItem = _.findWhere(arr, {id: result.id});
            //selectedItem.selected = !selectedItem.selected;
        };

        $scope.saveQuery = function() {
            var form = $scope.queryForm,
                channelForm = {};

            /**
             *  'TWITTER_SEARCH': 101,
             *  'TWITTER_ACCOUNT': 102,
             *  'FACEBOOK_GROUP': 201,
             *  'FACEBOOK_PAGE': 202,
             *  'GOOGLE_PLUS_SEARCH': 301,
             *  'YOUTUBE_CHANNEL': 401,
             *  'YOUTUBE_KEYWORD': 402,
             *  'INSTAGRAM_ACCOUNT': 501
             **/

            // Should use the ChannelTypesObj get network function later.
            var selectedStream = _.where($scope.streamResults, {
                selected: true
            });
            if (form.smChannel.id === 202 || form.smChannel.id === 401) {
                channelForm = {
                    type: form.smChannel.id,
                    identifier: form.query.id,
                    'stream_type': parseInt(selectedStream[0].id)
                };
            } else if (form.smChannel.id === 102) {
                channelForm = {
                    type: form.smChannel.id,
                    identifier: form.query['id_str'],
                    'stream_type': parseInt(selectedStream[0].id)

                };
            } else if (form.smChannel.id === 201) {
                channelForm = {
                    type: form.smChannel.id,
                    identifier: form.query.id,
                    token: form.smChannel.token.id,
                    'stream_type': parseInt(selectedStream[0].id)

                };
            } else if (form.smChannel.id === 501) {
                channelForm = {
                    type: form.smChannel.id,
                    identifier: form.query.username,
                    'stream_type': parseInt(selectedStream[0].id)

                };
            } else {
                channelForm = {
                    type: form.smChannel.id,
                    identifier: form.query,
                    'stream_type': parseInt(selectedStream[0].id)

                };

            }
            var channelPromise = Channels.post(channelForm).$promise;

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

                angular.forEach(selectedUsers, function(user) {
                    form.users.push(user.id);
                });
                // Pust the logged in user to the form silently,
                // Because he should have the added query implicitly
                form.users.push($rootScope.user.id);

                angular.forEach(selectedDicts, function(dict) {
                    form.dictionaries.push(dict.id);
                });

                angular.forEach(selectedApps, function(app) {
                    form[app['application']] = true;
                });

                form['sm_channel'] = channel.id;
                var queryPromise = Queries.post(form).$promise;

                queryPromise.then(function() {
                    Flash.show('query added successfully', 'success');
                    $state.go('index.allQueries');
                });

                queryPromise.catch(function(response) {
                    Errors.addErrors($scope, response.data);
                });
            });
        };

        $scope.getFacebookGroups = function(tokenId) {
            var fbGroupsPromise = FbGroups.get({
                id: tokenId
            }).$promise;

            fbGroupsPromise.then(function(groups) {
                $scope.groups = groups;
            });
        };

        $scope.clearSearch = function() {
            $scope.queryForm.query = '';
            $scope.queryForm.searchText = '';
            $scope.queryForm.smChannel = false;
            $scope.twitterResults = {};
            $scope.facebookResults = {};
            $scope.selected = [];
            $scope.validQuery = false;
        };

        /**************************** Edit Query view ************************/

        if (!_.isEmpty(queryClone)) {
            var query = $scope.query = queryClone;

            // Construct the apps object for this query
            // to be able to select it
            query.apps = GetUserApps.constructObj(query.apps);
            query.dictionaries = DictObj.constructDictObject(query.dictionaries);

            query.apps.forEach(function(app) {
                $scope.selectItem(app, $scope.applicationResults);
            });

            $scope.smChannelName = ChannelTypesObj.getNetworkById(queryClone['sm_channel'].type).displayName;

            $scope.cancel = function() {
                $uibModalInstance.close();
            };

            $scope.save = function() {
                var form = {},
                    channelForm = {};

                angular.copy(query, form);

                var channelName = ChannelTypesObj.getNetworkById(form['sm_channel'].type).displayName;
                var selectedStream = _.where($scope.streamResults, {
                    selected: true
                });
                channelForm = {
                    type: form['sm_channel'].type,
                    identifier: form['sm_channel'].identifier,
                    streamType: selectedStream.id
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
        }
    });
})();
