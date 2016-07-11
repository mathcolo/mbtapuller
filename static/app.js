var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']);


app.controller('appCtrl', function ($http, $mdSidenav, $location) {

  this.go = function (name, id) {
	console.log(name);
    $location.path("/trains/" + name + "/id/" + id);
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
            .when('/trains/:route_name/id/:route_id', {
                templateUrl : 'static/partials/route.html',
				controller  : 'routeController'
            })
			.otherwise({
                 redirectTo: '/'
             });
			
	});	
  





