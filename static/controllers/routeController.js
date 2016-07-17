app.controller('routeController', function ($scope, $routeParams, $http) {
    'use strict';
	
	$scope.route = $routeParams.route_name;
	
	$scope.getData = function(route_id) {
		$http.get('/trains/' + route_id)
		.then(function successCallback(response) {
				$scope.trains = response.data;
			}, function errorCallback(response) {
		});
		
		$http.get('/stations/' + route_id)
		.then(function successCallback(response) {
				$scope.stations = response.data;
				
				var stations_length = $scope.stations.length;
				
				$scope.first = $scope.stations[0].name;
				$scope.last = $scope.stations[stations_length - 1].name;
				
				$scope.destination = true;
				
			}, function errorCallback(response) {
				
		});
	};
	
	$scope.init = function() {
		$http.get('/id?name=' + $scope.route)
		.then(function successCallback(response) {
				var route_id = parseInt(response.data);
				$scope.getData(route_id);
			}, function errorCallback(response) {
		});
		
		
	};
	
	$scope.changeDestination = function(destination) {
		if (destination != $scope.destination) {
			$scope.destination = destination;
			$scope.stations = $scope.stations.reverse();
		}
	};
	
	$scope.init();
	
});
