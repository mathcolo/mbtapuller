app.controller('routeController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route_id = $routeParams.route_id;
	
	$http.get('/get' + $routeParams.route_id + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
		}, function errorCallback(response) {
	});
	
	$http.get('/stations/' + $routeParams.route_id)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
		}, function errorCallback(response) {
			
	});
});
