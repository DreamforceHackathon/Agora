var app = angular.module('Agora', [
  "ngRoute",
  "ngTouch",
  "ngAnimate",
  "mobile-angular-ui"
]);

app.config(function($routeProvider, $locationProvider) {
  $routeProvider.when('/',          {templateUrl: "topics.html"});
  $routeProvider.when('/:category', {templateUrl: "topics.html"});
  $routeProvider.when('/:category/:topic',    {templateUrl: "posts.html"}); 
  $routeProvider.when('/login',      {templateUrl: "accordion.html"}); 
  $routeProvider.when('/register', {templateUrl: "register.html"}); 
});

app.controller('MainController', function($rootScope, $scope, $location, $http){

  $rootScope.animationClass = "slide-left";

  $rootScope.$on("$routeChangeStart", function(){
    $rootScope.loading = true;
  });

  $rootScope.$on("$routeChangeSuccess", function(){
    $rootScope.loading = false;
  });

  $scope.chatUsers = [
    { name: "Carlos  Flowers", online: true },
    { name: "Byron Taylor", online: true },
  ];

  $http.get('http://beautiful-mermaids.herokuapp.com/agora/api/v1.0/categories').
  success(function(data, status, headers, config) {
    $scope.categories = data.categories;
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
});

app.controller('topicControl', function($rootScope, $scope, $routeParams, $location, $http){

  if($routeParams.category != undefined){
    $scope.$routeParams = $routeParams;
  }

  else{
    $scope.$routeParams = {category: "Local"};
  }

  $http.get('http://beautiful-mermaids.herokuapp.com/agora/api/v1.0/topics/'+ $scope.$routeParams.category).
    success(function(data, status, headers, config) {
      $scope.topics = data.topics;
    }).
    error(function(data, status, headers, config) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
  });

  $scope.leftTransition = function(path) {
    $rootScope.animationClass = "slide-left";
    $location.path($routeParams.category+'/'+path);
  }
});

app.controller('postControl', function($rootScope, $scope, $routeParams, $location, $http){

  $scope.$routeParams = $routeParams;

  $scope.backToCat = function() {
    $rootScope.animationClass = "slide-right";
    $location.path($routeParams.category);
  }

  $http.get('http://beautiful-mermaids.herokuapp.com/agora/api/v1.0/topic/'+ $scope.$routeParams.topic).
    success(function(data, status, headers, config) {
      $scope.posts = data.topic[0].posts;
      $scope.topicName = data.topic[0].Name;
      $scope.topicBody = data.topic[0].Topic_Body__c;
      $scope.uglyTopicId = data.topic[0].Id;
    }).
    error(function(data, status, headers, config) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
  });

  $scope.sendPost = function() {

    var data = {
      Topic_ID__c: $scope.uglyTopicId, 
      Post_User__c: "003o000000BTVrE",
      Position__c: $scope.position, 
      Post_Body__c: $scope.newPostBody
    };

    console.log(data);

    $.post('http://beautiful-mermaids.herokuapp.com/agora/api/v1.0/newpost', data, function(response){
      console.log(response);
    });
  }
});