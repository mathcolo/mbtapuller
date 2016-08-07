app.controller('favoritesController', function ($scope, $localStorage, $http, FavoritesService, UtilityService, $interval) {
    'use strict';
	
	
	$scope.addToFavorites = function(station_id) {
		if (FavoritesService.favoritesExist()) {

			var index = $localStorage.favorite_stations.indexOf(station_id);
			
			if (index < 0)
				$localStorage.favorite_stations.push(station_id);
			else {
				if ($localStorage.favorite_stations.length === 1)
					delete $localStorage.favorite_stations;
				
				else {
					$localStorage.favorite_stations.splice(index, 1);
				}
				
				for (var i = 0; i < $scope.stations.length; i++) {
					if ($scope.stations[i].id === station_id)
						$scope.stations.splice(i, 1);
				}
			
			}
		}
		else {
			$localStorage.favorite_stations = [station_id];			
		}
	};
	
	$scope.favoritesExist = FavoritesService.favoritesExist;
	$scope.isFavorited = FavoritesService.isFavorited;

	$scope.predictionText = function(station_id) {
		var str = "";
		
		for (var i = 0; i<$scope.stations.length; i++) {
			
			var o_pre_1 = $scope.stations[i].outbound_pre.pre_1;
			var o_pre_2 = $scope.stations[i].outbound_pre.pre_2;
			var i_pre_1 = $scope.stations[i].inbound_pre.pre_1;
			var i_pre_2 = $scope.stations[i].inbound_pre.pre_2;
			
			if ($scope.stations[i].id === station_id) {
				if (o_pre_2 === null) {
					if (o_pre_1 === null) {
						 str = "Outbound: There is no scheduled service to this station at this time.<br />";
					}
					else {
						str = "Next Service - Outbound: " + UtilityService.formatSeconds(o_pre_1) + "<br />";
					}
				}
				else {
				str = "Next Service - Outbound: " + UtilityService.formatSeconds(o_pre_1) + ", " + UtilityService.formatSeconds(o_pre_2) + "<br />";
				}
				
				if (i_pre_2 === null) {
					if (i_pre_1 === null) {
						 str += "Next Service - Inbound: There is no scheduled service to this station at this time.";
						break;
					}
					else {
						str += "Next Service - Inbound: " + UtilityService.formatSeconds(i_pre_1);
						break;
					}
				}
				str += "Inbound: " + UtilityService.formatSeconds(i_pre_1) + ", " + UtilityService.formatSeconds(i_pre_2) + ".";
				break;
			}
		}
		
		return str;
	}

	$scope.refreshData = function() {
		angular.forEach($scope.stations, function(value, key){
			 $http.get('/station/' + value.id + '/direction/' + 0 + '/nextservice')
			 .then(function successfulCallback(response) {
				 $scope.stations[key].outbound_pre.pre_1 = response.data['prediction_1'];
				 $scope.stations[key].outbound_pre.pre_2 = response.data['prediction_2'];

			 }, function errorCallback(response) {
			});

			$http.get('/station/' + value.id + '/direction/' + 1 + '/nextservice')
			 .then(function successfulCallback(response) {
				 $scope.stations[key].inbound_pre.pre_1 = response.data['prediction_1'];
				 $scope.stations[key].inbound_pre.pre_2 = response.data['prediction_2'];

			 }, function errorCallback(response) {
			});
		});
	};

	$scope.init = function() {
		$scope.stations = [];
	
		if (FavoritesService.favoritesExist()) {
			for (var i = 0; i < $localStorage.favorite_stations.length; i++) {
				$http.get('/station/' + $localStorage.favorite_stations[i])
					.then(function successCallback(response) {
					$scope.stations.push(response.data);
				}, function errorCallback(response) {

			});
			}
		}
	}
	
	$scope.init();
	$interval($scope.refreshData, 60000);
	
});
