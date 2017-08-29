(function() {
    'use strict';
    var pieChartDirective = angular.module('rootApp.directives');
    pieChartDirective.directive('cPie', function() {
        return {
            restrict: 'E',
            scope: {
                data: '=',
            },
            link: function(scope, element, attrs) {
                var colors = d3.scale.category10();
                var svg = d3.select(element[0])
                    .append("svg");
                scope.$watch('data', function(newVal, oldVal) {
                    if (newVal) {
                        var chart = nv.models.pieChart()
                            .x(function(d) {
                                return d.key;
                            })
                            .y(function(d) {
                                return d.value;
                            })
                            .color(colors.range())
                            .margin({
                                left: 0,
                                right: 0
                            })
                            .tooltipContent(function(key, y, e, graph) {
                                return '<h3 class"pie-tooltip-h3">' + key + '</h3>' + '<p class"pie-tooltip-p">' + e.value + '</p>';
                            })
                            .showLabels(true)
                            .labelType("percent")
                            .labelThreshold(0.05);

                        d3.select("#pie-chart svg")
                            .datum(scope.data)
                            .transition().duration(350)
                            .call(chart);

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
