(function () {
  'use strict';
  // TODO: replace ngRoute with ui.router

  angular
    .module('authentication', ['ngCookies', 'ui.router']);

angular
    .module('authentication')
    .config(config);

  config.$inject = ['$stateProvider', '$urlRouterProvider', '$locationProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider.otherwise('/home')
    $stateProvider

    .state('register', {
      url: '/register',
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/components/authentication/templates/register.html'
    })

    .state('login', {
      url: '/login',
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/components/authentication/templates/login.html'
    })

    // Enable HTML5 routing
    $locationProvider.html5Mode(true);

    // For the benefit of search engines
    $locationProvider.hashPrefix('!');
  }


  angular
  .module('authentication')
  .run(run);

run.$inject = ['$http'];

/**
* @name run
* @desc Update xsrf $http headers to align with Django's defaults
*/
function run($http) {
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.xsrfCookieName = 'csrftoken';
}
})();