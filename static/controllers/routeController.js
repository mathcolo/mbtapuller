app.controller('routeController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route_name = $routeParams.route_name;
	
	$http.get('/get' + $routeParams.route_name + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
		}, function errorCallback(response) {
	});
	
	$http.get('/stations/' + $routeParams.route_name)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
		}, function errorCallback(response) {
			
	});
});
