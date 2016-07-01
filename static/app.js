var app = angular.module('mbtaApp', []);


app.controller('navCtrl', function ($scope, $window) {
  $scope.currentPage = "";
  $scope.go = function (page) {
    var url = "http://" + $window.location.host + "/" + page;
	$window.location.href = url;
  };
});