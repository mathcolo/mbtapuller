var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']);


app.controller('appCtrl', function ($http, $mdSidenav, $location) {

  this.go = function (name, id) {
    $location.path("/trains/" + name + "/id/" + id);
  };
  
  this.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };
  
});

app.factory('httpErrorResponseInterceptor', ['$q', '$location',
  function($q, $location) {
    return {
      response: function(responseData) {
        return responseData;
      },
      responseError: function error(response) {
        switch (response.status) {
          case 404:
            $location.path('/404');
            break;
          default:
            $location.path('/error');
        }

        return $q.reject(response);
      }
    };
  }
]);

app.config(['$httpProvider',
  function($httpProvider) {
    $httpProvider.interceptors.push('httpErrorResponseInterceptor');
  }
]);

// configure our routes
app.config(function($routeProvider) {
	$routeProvider

		.when('/trains/:route_name/id/:route_id', {
			templateUrl : 'static/partials/route.html',
			controller  : 'routeController'
		})
		.when('/404', {
			templateUrl : 'static/partials/404.html'
		})
		.when('/error', {
			templateUrl : 'static/partials/error.html'
		})
		.otherwise({
			 redirectTo: '/'
		 });
		
});	

// configure our routes
app.config(function($routeProvider) {
	$routeProvider

		.when('/trains/:route_name/id/:route_id', {
			templateUrl : 'static/partials/route.html',
			controller  : 'routeController'
		})
		.otherwise({
			 redirectTo: '/'
		 });
		
});	

  





