app.controller('routeController', function ($scope, $routeParams, $http, FavoritesService, UtilityService, $interval, PredictionService) {

    var vm = this;

    vm.stations = [];
    vm.trains = [];
	vm.destination = true;
    vm.favoritesExist = FavoritesService.favoritesExist;
	vm.isFavorited = FavoritesService.isFavorited;
	vm.addToFavorites = FavoritesService.addToFavorites;
	
	var getData = function(route_id) {
        refreshTrains(route_id);
		
		$http.get('/stations/' + route_id)
		.then(function successCallback(response) {
				vm.station_ids = response.data;

				angular.forEach(vm.station_ids, function(value, key){
					 $http.get('/station/' + value + '/direction/' + (vm.destination ? 1 : 0 ) + '/details')
					 .then(function successfulCallback(response) {
						 vm.stations.push(response.data);
					 }, function errorCallback(response) {
					});
				});
			}, function errorCallback(response) {
				
		});
	};
	
	var getTerminalStations = function(route_id) {
		$http.get('/stations/' + route_id + '/terminal')
		.then(function successCallback(response) {
				vm.first = response.data['first'];
				vm.last = response.data['last'];
			}, function errorCallback(response) {
		});
	}
	
	var init = function() {
	    vm.route = $routeParams.route_name;
		$http.get('/route?name=' + vm.route)
		.then(function successCallback(response) {
				vm.route_id = parseInt(response.data);
				getData(vm.route_id);
				getTerminalStations(vm.route_id);
			}, function errorCallback(response) {
		});
		
		
	};

	var filterTrains = function(direction) {
		vm.trains = [];
			for (var i = 0; i < vm.allTrains.length; i++) {
				var train_direction = vm.allTrains[i]['direction'];
				if (train_direction == direction) {
					vm.trains.push(vm.allTrains[i]);
				}
			}
	}

	vm.changeDestination = function (destination) {
		if (destination != vm.destination) {
			filterTrains(destination);
			vm.stations = vm.stations.reverse();
			refreshData(vm.route_id);
			vm.destination = destination;
		}
	};


	var stationStatus = function(station) {
		var status = "NOTHING";
		for(var i = 0; i < vm.trains.length; i++) {
			if(vm.trains[i]['status'] == "AT_STATION" && vm.trains[i]['station_1'] == station['name']) {
				return "AT_STATION";
			}
			if(vm.trains[i]['station_2'] == station['name']) {
				return "IN_TRANSIT_TO";
			}
		}
		return status;
	}

	vm.styleForIconAtStation = function(station) {
		var status = stationStatus(station);
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
	
	var refreshData = function(route_id) {
		angular.forEach(vm.stations, function(value, key){
			 refreshPredictions(key, value);
		});	

		if (vm.route_id !== null) {
		    route_id = vm.route_id;
		}
		refreshTrains(route_id);
	};

	var refreshPredictions = function(key, value) {
	    $http.get('/station/' + value.id + '/direction/' + (vm.destination ? 1 : 0 ) + '/nextservice')
			 .then(function successfulCallback(response) {
				 vm.stations[key].pre_1 = response.data['prediction1'];
				 vm.stations[key].pre_2 = response.data['prediction2'];
			 }, function errorCallback(response) {
		});
	};

	var refreshTrains = function(route_id) {
	    $http.get('/trains/' + route_id)
		.then(function successCallback(response) {
				vm.allTrains = response.data;
				filterTrains(vm.destination);
			}, function errorCallback(response) {
		});
	}
	
	vm.predictionText = function(station_id) {
		for (var i = 0; i< vm.stations.length; i++) {
			if (vm.stations[i].id === station_id) {
			    return PredictionService.makePredictionString(vm.stations[i].pre_1, vm.stations[i].pre_2);
			}
		}
	}
	
	init();
	var refresh = $interval(refreshData, 60000);

	$scope.$on("$destroy", function() {
        if (refresh) {
            $interval.cancel(refresh);
        }
    });
	
});
