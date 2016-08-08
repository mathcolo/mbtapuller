app.controller('favoritesController', function ($scope, $localStorage, $http, FavoritesService, UtilityService, $interval, PredictionService) {
    var vm = this;
	
	vm.favoritesExist = FavoritesService.favoritesExist;
	vm.addToFavorites = function(station_id) {

		if (vm.favoritesExist()) {

			var index = $localStorage.favorite_stations.indexOf(station_id);

			if (index >= 0) {
				for (var i = 0; i < vm.stations.length; i++) {
					if (vm.stations[i].id === station_id)
						vm.stations.splice(i, 1);
				}
		    }
		}

		FavoritesService.addToFavorites(station_id);
	};

	vm.predictionText = function(station_id) {
		var str = "";
		
		for (var i = 0; i<vm.stations.length; i++) {
			if (vm.stations[i].id === station_id) {
                str += "Outbound: "
                    + PredictionService.makePredictionString(vm.stations[i].outbound_pre.pre_1,
                                                            vm.stations[i].outbound_pre.pre_2)
                    + "<br />";
                str += "Inbound: "
                    + PredictionService.makePredictionString(vm.stations[i].inbound_pre.pre_1,
                                                             vm.stations[i].inbound_pre.pre_2);
				return str;
			}
		}
	}

	var refreshFavoritesData = function() {
	    for (var i = 0; i < vm.stations.length; i++) {
            refreshOutboundPredictions(i);
            refreshInboundPredictions(i);
		}
	};

	var refreshInboundPredictions = function(station_idx) {
	    $http.get('/station/' + vm.stations[station_idx].id + '/direction/' + 1 + '/nextservice')
			 .then(function successfulCallback(response) {
				 vm.stations[station_idx].inbound_pre.pre_1 = response.data['prediction1'];
				 vm.stations[station_idx].inbound_pre.pre_2 = response.data['prediction2'];

			 }, function errorCallback(response) {
		    });
	}

	var refreshOutboundPredictions = function(station_idx) {
	    $http.get('/station/' + vm.stations[station_idx].id + '/direction/' + 0 + '/nextservice')
			 .then(function successfulCallback(response) {
				 vm.stations[station_idx].outbound_pre.pre_1 = response.data['prediction1'];
				 vm.stations[station_idx].outbound_pre.pre_2 = response.data['prediction2'];

			 }, function errorCallback(response) {
		    });
	}

	var init = function() {
		vm.stations = [];
	
		if (vm.favoritesExist()) {
			for (var i = 0; i < $localStorage.favorite_stations.length; i++) {
				stationDetails(i);
			}
		}
	}

	var stationDetails = function(station_idx) {
	    $http.get('/station/' + $localStorage.favorite_stations[station_idx])
					.then(function successCallback(response) {
					vm.stations.push(response.data);
				}, function errorCallback(response) {

		});
	}
	
	init();
	var refresh = $interval(refreshFavoritesData, 60000);

	$scope.$on("$destroy", function() {
        if (refresh) {
            $interval.cancel(refresh);
        }
    });
	
});
