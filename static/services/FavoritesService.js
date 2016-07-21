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
});