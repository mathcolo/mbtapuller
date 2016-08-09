app.service('PredictionService', function(UtilityService) {

    this.makePredictionString = function(pre1, pre2) {
        if (pre2 === null) {
			if (pre1 === null) {
				 return "There is no scheduled service to this station at this time.";
			}
			else {
				return "Next Service: " + UtilityService.formatSeconds(pre1);
			}
		}
		else {
			return "Next Service: " + UtilityService.formatSeconds(pre1) + ", " + UtilityService.formatSeconds(pre2);
		}
    }
});