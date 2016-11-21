(function () {

'use strict';

    angular
        .module('authentication')
        .controller('RegisterController', RegisterController);


    RegisterController.$inject = ['$location', 'Authentication']

    function RegisterController($location, Authentication) {
        var vm = this;

        vm.register = register;

        activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf authentication.controllers.RegisterController
         */
        function activate() {
          // If the user is authenticated, they should not be here.
          if (Authentication.isAuthenticated()) {
            $location.url('/');
          }
        }

        function register() {
            Authentication.register(vm.email, vm.password)
        }
    }

})();