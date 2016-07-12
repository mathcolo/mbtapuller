app.controller('routeController', function ($scope, $routeParams, $http, $rootScope) {
    'use strict';

	$scope.route_id = $rootScope.trainRoutes.filter(function(routeObject) {return routeObject["name"] == $routeParams.route_name})[0]["id"]

	$http.get('/get' + $scope.route_id + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
		}, function errorCallback(response) {
	});
	
	$http.get('/stations/' + $scope.route_id)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
			var stations_length = $scope.stations.length;
			
			$scope.first = $scope.stations[0].name;
			$scope.last = $scope.stations[stations_length - 1].name;
			
			$scope.destination = true;
		
			
			
		}, function errorCallback(response) {
			
	});
	
	$scope.changeDestination = function(destination) {
		if (destination != $scope.destination) {
			$scope.destination = destination;
			$scope.stations = $scope.stations.reverse();
		}
		
		
	
	};
});
