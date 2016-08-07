app.service('UtilityService', function() {

    this.formatSeconds = function(seconds) {

        var mins = Math.floor(seconds/60);
        var secs = seconds - (mins*60);

        if (secs < 10) {
            return mins + ":0" + secs;
        }

        return mins + ":" + secs;
    };

});