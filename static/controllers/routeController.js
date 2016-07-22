app.controller('routeController', function ($scope, $routeParams, $localStorage, $http, FavoritesService) {
    'use strict';
	
	$scope.route = $routeParams.route_name;
	
	$scope.favoritesExist = FavoritesService.favoritesExist;
	$scope.isFavorited = FavoritesService.isFavorited;
	
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


	$scope.stationStatus = function(station) {
		var status = "NOTHING";

		for(var i = 0; i < $scope.trains.length; i++) {
			if ($scope.trains[i]['destination'] != $scope.stations[$scope.stations.length-1]['id'])
				continue;

			if($scope.trains[i]['status'] == "AT_STATION" && $scope.trains[i]['station_1'] == station['name']) {
				return "AT_STATION";
			}

			if($scope.trains[i]['station_2'] == station['name']) {
				return "IN_TRANSIT_TO";
			}
		}

		return status;

	}

	$scope.styleForIconAtStation = function(station) {
		//return "visibility: hidden;";
		var status = $scope.stationStatus(station);
		switch(status) {
			case "NOTHING":
				return "visibility: hidden;";
				break;
			case "AT_STATION":
				return "";
				break;
			case "IN_TRANSIT_TO":
				return "background-color: red;"
				break;
		}
	}

	$scope.trainBetween = function(station1, station2) {
		for(var i = 0; i < $scope.trains.length; i++) {
			if ($scope.trains[i]['destination'] != $scope.stations[$scope.stations.length-1]['id'])
				return false;

			if($scope.trains[i]['status'] != "IN_TRANSIT")
				return false;

			if($scope.trains[i]['station_1'] == station1['name'] && $scope.trains[i]['station_1'] == station2['name']) {
				return true;
			}

			if($scope.trains[i]['station_1'] == station2['name'] && $scope.trains[i]['station_1'] == station1['name']) {
				return true;
			}
		}
		return false;
	}

	$scope.trainAt = function(station) {
		for(var i = 0; i < $scope.trains.length; i++) {
			if($scope.trains[i]['status'] == "AT_STATION" && $scope.trains[i]['station_1'] == station['name'] && $scope.trains[i]['destination'] == $scope.stations[$scope.stations.length-1]['id']) {
				return true;
			}
		}
		return false;
	}
	
	$scope.addToFavorites = function(station_id) {
		if ($scope.favoritesExist()) {

			var index = $localStorage.favorite_stations.indexOf(station_id);
			
			if (index < 0)
				$localStorage.favorite_stations.push(station_id);
			else {
				if ($localStorage.favorite_stations.length === 1) {
					delete $localStorage.favorite_stations;
				}
				else {
					$localStorage.favorite_stations.splice(index, 1);
				}
			}
		}
		else {
			$localStorage.favorite_stations = [station_id];			
		}
	};
	
	
	$scope.init();
	
});
