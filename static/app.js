var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']);

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

		.when('/trains/:route_name', {
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

  





