app.controller('routeController', function ($scope, $routeParams, $localStorage, $http, FavoritesService, $interval) {
    'use strict';
	// need general service file to hold conversion of seconds to minutes and seconds
	
	$scope.route = $routeParams.route_name;
	$scope.trains = [];
	$scope.stations = [];
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
				$scope.station_ids = response.data;
				
				angular.forEach($scope.station_ids, function(value, key){
					 $http.get('/station/' + value + '/direction/' + ($scope.destination ? 1 : 0 ) + '/details')
					 .then(function successfulCallback(response) {
						 $scope.stations.push(response.data);
					 }, function errorCallback(response) {
					});
				});
			}, function errorCallback(response) {
				
		});
	};
	
	$scope.getTerminalStations = function(route_id) {
		$http.get('/stations/' + route_id + '/terminal')
		.then(function successCallback(response) {
				$scope.first = response.data['first'];
				$scope.last = response.data['last'];
			}, function errorCallback(response) {
		});
	}
	
	$scope.init = function() {
		$http.get('/id?name=' + $scope.route)
		.then(function successCallback(response) {
				$scope.route_id = parseInt(response.data);
				$scope.getData($scope.route_id);
				$scope.getTerminalStations($scope.route_id);
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
			$scope.refreshData();
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
				return "train_circle_hide";
				break;
			case "AT_STATION":
				return "train_circle_at_station";
				break;
			case "IN_TRANSIT_TO":
				return "train_circle_in_transit"
				break;
		}
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
	
	$scope.refreshData = function() {
		angular.forEach($scope.stations, function(value, key){
			 $http.get('/station/' + value.id + '/direction/' + ($scope.destination ? 1 : 0 ) + '/nextservice')
			 .then(function successfulCallback(response) {
				 $scope.stations[key].pre_1 = response.data['prediction1'];
				 $scope.stations[key].pre_2 = response.data['prediction2'];
			 }, function errorCallback(response) {
			});
		});	
		
		$http.get('/trains/' + $scope.route_id)
		.then(function successCallback(response) {
				$scope.allTrains = response.data;
				$scope.filterTrains($scope.destination);
			}, function errorCallback(response) {
		});
	};
	
	$scope.predictionText = function(station_id) {
		var str = "";
		for (var i = 0; i<$scope.stations.length; i++) {
			if ($scope.stations[i].id === station_id) {
				if ($scope.stations[i].pre_2 === null) {
					if ($scope.stations[i].pre_1 === null) {
						 str = "There is no scheduled service to this station at this time.";
						break;
					}
					else {
						str = "Next service: " + $scope.stations[i].pre_1 + " seconds away";
						break;
					}
				}
				str = "Next service: " + $scope.stations[i].pre_1 + " seconds away  | " + $scope.stations[i].pre_2 + " seconds away";
				break;
			}
		}
		
		return str;
	}
	
	
	$scope.init();
	$interval($scope.refreshData, 60000);
	
});
