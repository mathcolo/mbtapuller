app.controller('routeController', function ($scope, $routeParams, $http) {

    $scope.route_id = $routeParams.route_id;
	
	$http.get('/get' + $routeParams.route_id + 'Trains')
	.then(function successCallback(response) {
			$scope.trains = response.data;
		}, function errorCallback(response) {
	});
	
	$http.get('/stations/' + $routeParams.route_id)
	.then(function successCallback(response) {
			$scope.stations = response.data;
			
			var stations_length = $scope.stations.length;
			
			$scope.first = $scope.stations[0].name;
			$scope.last = $scope.stations[stations_length - 1].name;
			
			console.log($scope.first);
			console.log($scope.last);
			
			$scope.destination = $scope.last;
		
			
			
		}, function errorCallback(response) {
			
	});
	
	$scope.changeDestination = function(destination) {
		console.log($scope.destination);
		if ($scope.destination == $scope.first) {
			$scope.destination = $scope.last;
		}
		else {
			$scope.destination = $scope.first;
		}
		
		$scope.stations = $scope.stations.reverse();
	
	};
});
