var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']);


app.controller('appCtrl', function ($http, $mdSidenav, $location) {

  this.go = function (page) {
    $location.path("/trains/" + page);
  };
  
  this.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
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
			
	});	
  





