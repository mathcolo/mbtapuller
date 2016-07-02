app.controller('allRouteController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route = $routeParams.route;
	
	$http.get('/getAllTrains')
    .then(function(response) {
        $scope.trains = response.data;
    });
});