app.service('FavoritesService', function($localStorage) {
    this.favoritesExist = function() {
		return $localStorage.favorite_stations;	
    }
	
	this.isFavorited = function(station_id) {
		if (this.favoritesExist()) {
			var index = $localStorage.favorite_stations.indexOf(station_id);
			
			return index > -1;
		}
		
		return false;
	}

	this.addToFavorites = function(station_id) {
		if (this.favoritesExist()) {

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
	}
});