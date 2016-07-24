app.controller('routeController', function ($scope, $routeParams, $localStorage, $http, FavoritesService) {
    'use strict';
	
	$scope.route = $routeParams.route_name;
	$scope.trains = [];
	$scope.destination = true;
	
	$scope.favoritesExist = FavoritesService.favoritesExist;
	$scope.isFavorited = FavoritesService.isFavorited;
	
	$scope.getData = function(route_id) {
		$http.get('/trains/' + route_id)
		.then(function successCallback(response) {
				$scope.allTrains = response.data;
				$scope.filterTrains($scope.destination);
			}, function errorCallback(response) {
		});
		
		$http.get('/stations/' + route_id)
		.then(function successCallback(response) {
				$scope.stations = response.data;
				
				var stations_length = $scope.stations.length;
				
				$scope.first = $scope.stations[0].name;
				$scope.last = $scope.stations[stations_length - 1].name;
				
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

	$scope.filterTrains = function(direction) {
		$scope.trains = [];
			for (var i = 0; i < $scope.allTrains.length; i++) {
				var train_direction = $scope.allTrains[i]['direction'];
				if (train_direction == direction) {
					$scope.trains.push($scope.allTrains[i]);
				}
			}
	}

	$scope.changeDestination = function (destination) {
		if (destination != $scope.destination) {
			$scope.filterTrains(destination);
			$scope.stations = $scope.stations.reverse();
			$scope.destination = destination;
		}
	};


	$scope.stationStatus = function(station) {
		var status = "NOTHING";

		for(var i = 0; i < $scope.trains.length; i++) {
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
		var status = $scope.stationStatus(station);
		switch(status) {
			case "NOTHING":
				return "visibility: hidden;";
				break;
			case "AT_STATION":
				return "background-color: purple; top: 40px;";
				break;
			case "IN_TRANSIT_TO":
				return "background-color: orange; bottom: 30px;"
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
