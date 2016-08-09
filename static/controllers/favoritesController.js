app.controller('favoritesController', function ($scope, $localStorage, $http, FavoritesService) {
    'use strict';
	
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
	
	
});
