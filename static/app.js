var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']);


app.controller('appCtrl', function ($http, $mdSidenav, $location, $rootScope) {

    $http.get('/routes')
	.then(function successCallback(response) {
        $rootScope.trainRoutes = response.data;
        $rootScope.trainRoutes.sort(function(a,b) {return (a["name"] > b["name"]) ? 1 : ((b["name"] > a["name"]) ? -1 : 0);} );
		}, function errorCallback(response) {
	});

  this.go = function (name) {
	console.log(name);
    $location.path("/trains/" + name);
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
            .when('/trains/:route_name', {
                templateUrl : 'static/partials/route.html',
				controller  : 'routeController'
            })
			.otherwise({
                 redirectTo: '/'
             });
			
	});	
  





