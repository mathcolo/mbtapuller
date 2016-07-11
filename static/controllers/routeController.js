app.controller('routeController', function ($scope, $routeParams, $http, $rootScope) {
    'use strict';

	for(var index in $rootScope.trainRoutes) {
		var routeObject = $rootScope.trainRoutes[index];
			if (routeObject["name"] == $routeParams.route_name) {
				$scope.route_id = routeObject["id"];
			}
	}
	
	$http.get('/get' + $scope.route_id + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
		}, function errorCallback(response) {
	});
	
	$http.get('/stations/' + $scope.route_id)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
		}, function errorCallback(response) {
			
	});
});
