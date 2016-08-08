var app = angular.module('mbtaApp', ['ngRoute', 'ngMaterial', 'ngMdIcons', 'ngStorage', 'ngSanitize']);


app.controller('appCtrl', function ($http, $mdSidenav, $mdDialog, $location) {

  this.go = function (path) {
    $location.path(path);
  };
  
  this.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  this.openMap = function() {
    $mdDialog.show({
      templateUrl: 'static/partials/transitmap.html',
      parent: angular.element(document.body),
      clickOutsideToClose:true,
      controller: DialogController,
      fullscreen: true
    });
  };

});

function DialogController($scope, $mdDialog) {
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
}


// configure our routes
app.config(function($routeProvider) {
	$routeProvider

		.when('/trains/:route_name', {
			templateUrl : 'static/partials/route.html',
			controller: '',
			controllerAs: ''
		})
		.when('/favorites', {
			templateUrl : 'static/partials/favorites.html',
			controller  : 'favoritesController'
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

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .accentPalette('blue-grey');
});
  





