app.controller('allRouteController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route = $routeParams.route;
	
	$http.get('/getAllTrains')
    .then(function successCallback(response) {
			$scope.trains = response.data;
			$scope.status = response.status;
		}, function errorCallback(response) {
			$scope.status = response.status;
	});
	
	$http.get('/stations/all')
    .then(function successCallback(response) {
			$scope.stations = response.data;
			
		}, function errorCallback(response) {
			
	});
});