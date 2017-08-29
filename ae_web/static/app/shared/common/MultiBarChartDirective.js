(function() {
    'use strict';
    var module = angular.module('rootApp.directives');

    var getFormatedData = function(data, fields, xField, getColorValue) {
        var formatedData = [];

        angular.forEach(fields, function(field, i) {
            formatedData.push({
                key: field.title,
                color: getColorValue(field.color),
                values: []
            });
            angular.forEach(data, function(value, j) {
                formatedData[i].values.push({
                    x: value[xField.name],
                    y: value[fields[i].name]
                });
            });
        });
        return formatedData;
    };

    module.directive('multiBarChart', function($rootScope) {
        return {
            restrict: 'E',
            scope: {
                'data': '=',
                't': '=',
                'fields': '=',
                'xaxis': '='
            },
            link: function(scope, element, attrs) {
                scope.$watch('data', function(newVal, oldVal) {
                    var height = 410;
                    var svg = d3.select(element[0])
                        .append("svg");
                    element.children().attr('height', height);
                    nv.addGraph(function() {
                        var chart = nv.models.multiBarChart()
                            .height(height)
                            .stacked(false)
                            .showLegend(false)
                            .transitionDuration(1)
                            .reduceXTicks(true) //If 'false', every single x-axis tick label will be rendered.
                            .rotateLabels(0) //Angle to rotate x-axis labels.
                            .showControls(false) //Allow user to switch between 'Grouped' and 'Stacked' mode.
                            .groupSpacing(0.1); //Distance between each group of bars.

                        if (scope.t === 'stacked') {
                            chart.stacked(true);
                        }
                        chart.xAxis.axisLabel(scope.xaxis.title);

                        var myData = getFormatedData(scope.data, scope.fields, scope.xaxis, $rootScope.getColorValue); //You need data...

                        d3.select(element.children()[0]) //Select the <svg> element you want to render the chart in.
                            .datum(myData) //Populate the <svg> element with chart data...
                            .call(chart); //Finally, render the chart!

                        //Update the chart when window resizes.
                        nv.utils.windowResize(function() {
                            chart.update();
                        });


                        return chart;
                    });

                });
            }
        };
    });
})();
