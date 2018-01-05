(function () {
  'use strict';

  angular
    .module('myApp')
    .config(config);

  config.$inject = ['$stateProvider', '$urlRouterProvider'];
// config.$inject = []
  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider

    .state('home', {
        url: '/home',
        templateUrl: '/static/templates/home.html'
    })

  }
})();