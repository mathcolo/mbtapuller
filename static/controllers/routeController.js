app.controller('routeController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route = $routeParams.route;
	
	$http.get('/get' + $routeParams.route + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
			$scope.status = response.status;
		}, function errorCallback(response) {
			$scope.status = response.status;
	});
	
	$http.get('/stations/' + $routeParams.route)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
		}, function errorCallback(response) {
			
	});
});
