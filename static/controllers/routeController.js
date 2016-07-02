app.controller('routeController', function ($scope, $routeParams, $http) {
    'use strict';
    $scope.route = $routeParams.route;
	
	$http.get('/get' + $routeParams.route + 'Trains')
    .then(function(response) {
        $scope.trains = response.data;
    });

});