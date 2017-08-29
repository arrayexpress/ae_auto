(function() {
    'use strict';
    var module = angular.module('rootApp.directives');

    var getWordsArray = function(wordsCount) {
        var words = [];
        angular.forEach(wordsCount, function(count, word) {
            words.push(word);
        });
        console.log(words);
        return words;
    };

    module.directive('wordCloud', function($rootScope) {
        return {
            restrict: 'E',
            scope: {
                'data': '=',
            },
            link: function(scope, element, attrs) {
                scope.$watch('data', function(newVal, oldVal) {
                    getWordsArray(scope.data);
                    var width = 1100;
                    var height = 650;

                    var fill = d3.scale.category20();
                    var draw = function(words) {
                        d3.select(element[0]).append("svg")
                            .attr("width", width)
                            .attr("height", height)
                            .append("g")
                            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
                            .selectAll("text")
                            .data(words)
                            .enter().append("text")
                            .style("font-size", function(d) {
                                return d.size + "px";
                            })
                            .style("font-family", "Impact")
                            .style("fill", function(d, i) {
                                return fill(i);
                            })
                            .attr("text-anchor", "middle")
                            .attr("transform", function(d) {
                                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                            })
                            .text(function(d) {
                                return d.text;
                            });
                    };

                    d3.layout.cloud().size([width, height])
                        .words(getWordsArray(scope.data).map(function(d) {
                            console.log(d);
                            console.log(scope.data[d]);
                            return {
                                text: d,
                                size: scope.data[d]
                            };
                        }))
                        .padding(5)
                        .rotate(function() {
                            // return ~~(Math.random() * 2) * 90;
                            return 0;
                        })
                        .font("Impact")
                        .fontSize(function(d) {
                            return d.size;
                        })
                        .on("end", draw)
                        .start();
                });
            }
        };
    });
})();
