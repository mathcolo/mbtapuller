app.controller('routeController', function ($scope, $routeParams, $localStorage, $http) {
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
	
	$scope.addToFavorites = function(station_id) {
		if ($scope.favoritesExist()) {

			var index = $localStorage.favorite_stations.indexOf(station_id);
			
			if (index < 0)
				$localStorage.favorite_stations.push(station_id);
			else {
				if ($localStorage.favorite_stations.length === 1)
					delete $localStorage.favorite_stations;
				
				else {
					$localStorage.favorite_stations.splice(index, 1);
				}
			}
		}
		else {
			$localStorage.favorite_stations = [station_id];			
		}
	};
	
	$scope.isFavorited = function(station_id) {
		if ($scope.favoritesExist()) {
			var index = $localStorage.favorite_stations.indexOf(station_id);
		
			return index > -1;
		}
		
		return false;
	}
	
	$scope.favoritesExist = function() {
		return localStorage.getItem("ngStorage-favorite_stations") !== null;	
	}
	
	
	$scope.init();
	
});
