app.service('TrainDisplayService', function(UtilityService) {

    var stationStatus = function(station, trains) {
		var status = "NOTHING";
		for(var i = 0; i < trains.length; i++) {
			if(trains[i]['status'] == "AT_STATION" && trains[i]['station_1'] == station['name']) {
				return "AT_STATION";
			}
			if(trains[i]['station_2'] == station['name']) {
				return "IN_TRANSIT_TO";
			}
		}
		return status;
	}

	this.styleForIconAtStation = function(station, trains) {
		var status = stationStatus(station, trains);
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

	this.tooltipForIconAtStation = function(station, trains)  {
		for(var i = 0; i < trains.length; i++) {
			if(trains[i]['status'] == "AT_STATION" && trains[i]['station_1'] == station['name']) {
				return "At " + station['name'];
			}
			if(trains[i]['station_2'] == station['name']) {
				return station['name'] + " in " + UtilityService.formatSeconds(station['pre_1']);
			}
		}
		return "";
	}
});