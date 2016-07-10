app.controller('allRouteController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route = $routeParams.route;
	
	$http.get('/getAllTrains')
    .then(function(response) {
        $scope.trains = response.data;
    });
	
	$http.get('/stations/all')
    .then(function(response) {
        $scope.stations = response.data;
    });
});