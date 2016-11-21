/**
* NavbarController
*/
(function () {
  'use strict';

  angular
    .module('myApp')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication) {
    var vm = this;

    vm.logout = logout;
    vm.test =  'test';

    /**
    * @name logout
    * @desc Log the user out
    */
    function logout() {
      Authentication.logout();
    }
  }
})();