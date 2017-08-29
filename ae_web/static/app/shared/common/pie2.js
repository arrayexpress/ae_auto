(function() {
    'use strict';
    var pieChartDirective = angular.module('rootApp.directives');
    var getColors = function(data, getColorValue) {
        var colorarray = [];
        angular.forEach(data, function(field) {
            colorarray.push(getColorValue(field.color));
        });
        return colorarray;
    };
    pieChartDirective.directive('cPie', function($rootScope) {
        return {
            restrict: 'E',
            scope: {
                data: '=',
                order: '='
            },
            link: function(scope, element, attrs) {
                var svg = d3.select(element[0]).append("svg");
                scope.$watch('data', function(newVal, oldVal) {
                    if (newVal) {
                        var chart = nv.models.pieChart().height(400).x(function(d) {
                            return d.key;
                        }).y(function(d) {
                            return d.value;
                        }).color(getColors(scope.data, $rootScope.getColorValue)).margin({
                            left: 0,
                            right: 0
                        }).tooltipContent(function(key, y, e, graph) {
                            return '<h3 class"pie-tooltip-h3">' + key + '</h3>' + '<p class"pie-tooltip-p">' + e.value + '</p>';
                        }).showLegend(false).showLabels(true).labelType("percent").labelThreshold(0.05);
                        d3.select("#pie-chart-" + scope.order + " svg").datum(scope.data).transition().duration(350).style("height", 400).call(chart);
                        chart.dispatch.on('stateChange', function(e) {
                            nv.log('New State:', JSON.stringify(e));
                        });
                        return chart;
                    }
                });
            }
        };
    });
})();
