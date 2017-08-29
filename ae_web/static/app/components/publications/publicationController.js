(function() {
    'use strict';
    var queryModule = angular.module('rootApp.publications.controllers');

    queryModule.controller('publicationsController', function($scope, $rootScope, $uibModal, Publications, Flash, EditPublicationStatus, Errors) {
        $scope.filteredTab = [{
                id:1,
                name: 'Already Connected',
                value: 'C'
            }];
        $scope._ = _;
        $scope.isCollapsed = true;
        //$scope.filterPublications($scope.filteredTab[0]);
        /*** Pagination settings ***/

        $scope.paginationSettings = {};
        $scope.paginationSettings.totalItems = 15;
        $scope.paginationSettings.currentPage = 1;
        $scope.size = 5;

        $scope.setPage = function (pageNo) {

            $scope.paginationSettings.currentPage = pageNo;
            //alert($scope.filteredTab[0]);
            console.log($scope.filteredTab);
            $scope.filterPublications($scope.filteredTab[0]);
            console.log('Page changed to: ' + $scope.paginationSettings.currentPage);

        };


        $scope.publicationTabs = [
            {
                id:1,
                name: 'Connected Automatically'

            },{
                id:2,
                name: 'Pending'

            },{
                id:3,
                name: 'Approved'

            },{
                id:4,
                name: 'Rejected'
            }
        ];


        $scope.publication_filters = [
            {
                id:1,
                 name: 'Already Connected',
                value: 'C'
            }, {
                id:2,
                name: 'New',
                value: 'N'

            },{
                id:3,
                name: 'Approved',
                value: 'A'


            },{
                id:4,name: 'Rejected',
                value: 'R'


            }

        ];



        var getPublications = function(filter) {
            var publicationPromise = Publications.get(filter).$promise;
            publicationPromise.then(function(response) {
                var publications = response.results;
                //alert(JSON.stringify(publications[0]));
                publications.forEach(function(p){
                    //console.log(p);
                    p.publication.whole_article = JSON.parse(p.publication.whole_article)
                    console.log(p.is_associated)
                });
                //console.log(publications[0].publication.whole_article.abstractText);
                // Pagination
                $scope.paginationSettings.totalItems = response.count;
                $scope.next = response.next;
                $scope.prev = response.prev;
                $scope.publications = publications;
                // Need to have an original copy of the publications,
                // so we can edit or delete later on

                //$scope.originalQueries = [];
                //angular.copy(publications, $scope.originalQueries);
                //
                //$scope.publications = QueryObj.constructQueryObject(publications);
            });
        };

        $scope.filterPublications = function(filter) {
            console.log('filter: ' + JSON.stringify(filter));
            //console.log();

            if (filter.value === 'C'){
                getPublications({
                'order_by': '-id',
                'associated':1,
                page: $scope.paginationSettings.currentPage
            });
            }
            else {
                getPublications({
                    'order_by': '-id',
                    'status': filter.value,
                    'associated': 0,
                    page: $scope.paginationSettings.currentPage
                });
            }
        };


        $scope.filterPublications($scope.filteredTab[0]);


        $scope.filterTabs = function(tabId) {
            console.log($scope.filteredTab );
            if (!_.isEmpty($scope.filteredTab)) {
                if (tabId === $scope.filteredTab[0].id)
                {return;}
            }
            $scope.paginationSettings.currentPage = 1;
            //alert(tabId)
            switch (tabId) {
                case 1:
                    $scope.filterPublications(_.where($scope.publication_filters, {
                        id: 1
                    })[0]);
                    $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 1
                    });
                    break;
                case 2:
                    $scope.filterPublications(_.where($scope.publication_filters, {
                        id: 2
                    })[0]);
                    $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 2
                    });
                    break;
                case 3:
                    $scope.filterPublications(_.where($scope.publication_filters, {
                        id: 3
                    })[0]);
                    $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 3
                    });
                    break;
                case 4:
                     $scope.filterPublications(_.where($scope.publication_filters, {
                        id: 4
                    })[0]);
                $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 4
                    });
                    break;
                default:
                     $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 1
                    });
                    $scope.filterPublications(_.where($scope.publication_filters, {
                        id: 1
                    })[0]);
                    break;
            }
            // if the filtered tabs isnt empty(no the all queries tab), then we filter the channel according to the channel id

            if (_.isEmpty($scope.filteredTab)) {
                $scope.filteredTab = _.where($scope.publication_filters, {
                        id: 1
                    });
                $scope.filterPublications($scope.filteredTab[0]);
            }
             //console.log($scope.filteredTab[0]);

        };

        $scope.updateStatus = function(publication, status){
            console.log(JSON.stringify($scope.filteredTab));

            EditPublicationStatus.edit(publication.id, status)
                .success(function() {

                    //Flash.show('password successfully edited.', 'success', 3000);
                    $scope.filterPublications($scope.filteredTab[0]);
                })
                .error(function(error) {
                    Errors.addErrors($scope, error);
                    Flash.show('something went wrong.', 'error', 3000);
                });
        }

        $scope.deleteQuery = function(query) {
            $uibModal.open({
                templateUrl: '/static/app/shared/common/_confirmModal.html',
                controller: 'confirmModalController',
                size: 'sm',
                resolve: {
                    type: function() {
                        return 'Query';
                    }
                }
            });
            // The $on function returns a listerer destroyer so we need to catch it in a variable,
            // to call it after the delete promise is done
            // so it doesnt conflict with other destroy events on different controllers
            var removeListener = $rootScope.$on('destroyQuery', function() {
                var queryPromise = Queries.delete({
                    id: query.id
                }).$promise;

                queryPromise.then(function() {
                    $scope.publications.splice($scope.publications.indexOf(query), 1);

                    Flash.show('query deleted successfully', 'success', 3000);

                    removeListener();
                });
                queryPromise.catch(function(resp) {
                    Flash.show(resp, 'error', 3000);

                    removeListener();
                });
            });
        };

        $scope.openEditModal = function(query) {
            var queryClone = {};
            angular.copy(query, queryClone);
            $uibModal.open({
                templateUrl: '/static/app/components/queries/_editQuery.html',
                controller: 'addQueryController',
                size: 'lg',
                resolve: {
                    queryClone: function() {
                        return queryClone;
                    },
                    originalQuery: function() {
                        return query;
                    }
                }
            });
        };


    });
})();
