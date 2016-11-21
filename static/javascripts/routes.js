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

    .state('firstPage', {
        url: '/firstPage',
        templateUrl: '/static/templates/firstPage.html'
    })
    .state('secondPage', {
        url: '/secondPage',
        templateUrl: '/static/templates/secondPage.html'
    })
    .state('thirdPage', {
        url: '/thirdPage',
        templateUrl: '/static/templates/thirdPage.html'
    })
    .state('fourthPage', {
        url: '/fourthPage',
        templateUrl: '/static/templates/fourthPage.html'
    })
  }
})();