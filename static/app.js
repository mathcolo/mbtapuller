var app = angular.module('mbtaApp', ['ngRoute']);


app.controller('navCtrl', function ($scope, $location) {
  $scope.currentPage = "";
  $scope.go = function (page) {
    $location.path("/trains/" + page);
  };
});

	// configure our routes
    app.config(function($routeProvider) {
        $routeProvider

			.when('/trains/all', {
                templateUrl : 'static/partials/route.html',
				controller  : 'allRouteController'
            })
            .when('/trains/:route', {
                templateUrl : 'static/partials/route.html',
				controller  : 'routeController'
            })
			.otherwise({
                 redirectTo: '/'
             });
			
	})	