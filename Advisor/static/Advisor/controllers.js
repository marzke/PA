/**
 * Created by marzke on 2/14/15.
 */
var advisorApp = angular.module('advisorApp', []);

advisorApp.controller('courseListCtrl', function ($scope, $http) {
    $http.get('courses').success(function(data) {
    $scope.courses = data;
  });
});