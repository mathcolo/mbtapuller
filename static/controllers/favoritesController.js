app.controller('favoritesController', function ($scope, $localStorage, $http, FavoritesService) {
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
						str = "Outbound: " + o_pre_1 + " seconds away. <br />";
					}
				}
				str = "Outbound: " + o_pre_1 + " seconds away  | " + o_pre_2 + " seconds away.<br />";
				
				if (i_pre_2 === null) {
					if (i_pre_1 === null) {
						 str += "Inbound: There is no scheduled service to this station at this time.";
						break;
					}
					else {
						str += "Inbound: " + i_pre_1 + " seconds away.";
						break;
					}
				}
				str += "Inbound: " + i_pre_1 + " seconds away  | " + i_pre_2 + " seconds away.";
				break;
			}
		}
		
		return str;
	}
	
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
	
	
});
