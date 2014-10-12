var app = angular.module('Agora', [
  "ngRoute",
  "ngTouch",
  "mobile-angular-ui"
]);

app.config(function($routeProvider, $locationProvider) {
  $routeProvider.when('/',          {templateUrl: "topics.html"});
  $routeProvider.when('/:category', {templateUrl: "topics.html"});
  $routeProvider.when('/:category/:topic',    {templateUrl: "posts.html"}); 
  $routeProvider.when('/login',      {templateUrl: "accordion.html"}); 
  $routeProvider.when('/register', {templateUrl: "register.html"}); 
});

app.service('analytics', [
  '$rootScope', '$window', '$location', function($rootScope, $window, $location) {
    var send = function(evt, data) {
      ga('send', evt, data);
    }
  }
]);

app.controller('MainController', function($rootScope, $scope, analytics){

  $rootScope.$on("$routeChangeStart", function(){
    $rootScope.loading = true;
  });

  $rootScope.$on("$routeChangeSuccess", function(){
    $rootScope.loading = false;
  });

  var scrollItems = [];

  for (var i=1; i<=100; i++) {
    scrollItems.push("Item " + i);
  }

  $scope.scrollItems = scrollItems;
  $scope.invoice = {payed: true};
  
  $scope.userAgent =  navigator.userAgent;
  $scope.chatUsers = [
    { name: "Carlos  Flowers", online: true },
    { name: "Byron Taylor", online: true },
    { name: "Jana  Terry", online: true },
    { name: "Darryl  Stone", online: true },
    { name: "Fannie  Carlson", online: true },
    { name: "Holly Nguyen", online: true }
  ];

  $scope.categories = [
    {title: "Politics"},
    {title: "Games"},
    {title: "Stuff"}
  ];

});

app.controller('topicControl', function($scope, $routeParams){

  if($routeParams.category != undefined){
    $scope.$routeParams = $routeParams;
  }

  else{
    $scope.$routeParams = {category: "All"};
  }

  $scope.topics = [
    {id: 1234124124, title: "WASSUP", body:"Glen is a dingus"},
    {id: 111111111, title: "WASSUP2", body:"Glen is a dingus2"}
  ];
});

app.controller('postControl', function($scope, $routeParams){

  $scope.$routeParams = $routeParams;
  $scope.posts = [
    {user: "Kenneth", body:"Glen is a dingus", position: "against"},
    {user: "Glen", body:"Glen is a dingus2", position: "for"},
    {user: "Kenneth", body:"Glen isfasdf a dingus", position: "against"},
    {user: "Glen", body:"Glen is a asdfasdingus2", position: "for"},
    {user: "Kenneth", body:"Glen isasdfasdf a dingus", position: "against"},
    {user: "Glen", body:"Glen is a dingus2", position: "for"},
    {user: "Kenneth", body:"Glen asdfasfdis a dingus", position: "against"},
    {user: "Glen", body:"Glen is asdfasfa dingus2", position: "against"},
    {user: "Kenneth", body:"Glen is a dingus", position: "for"},
    {user: "Glen", body:"Glen iasdfasdfs a dingus2", position: "against"}
  ];
});