/**
* LoginController
* @namespace authentication.controllers
*/

(function () {
    'use strict';

    angular
        .module('authentication')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$http', '$location', '$scope', 'Authentication'];


    /**
    * @namespace LoginController
    */
    function LoginController($http, $location, $scope, Authentication) {
        var vm = this;

        vm.login = login;

        activate();

        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated
        * @menmberOf authentication.controllers.LoginController
        */
        function activate() {
            // Redirect the user to homepage if the are already authenticated
            if(Authentication.isAuthenticated()) {
                $location.url('/');
            }
        }

        /**
         * @name login
         * @desc Try to log in with email `email` and password `password`
         * @param {string} email The email entered by the user
         * @param {string} password The password entered by the user
         * @returns {Promise}
         * @memberOf authentication.services.Authentication
         */
        function login(email, password) {
          return $http.post('/api/v1/auth/login/', {
            email: vm.email, password: vm.password
          }).then(loginSuccessFn, loginErrorFn);

          /**
           * @name loginSuccessFn
           * @desc Set the authenticated account and redirect to index
           */
          function loginSuccessFn(data, status, headers, config) {
            Authentication.setAuthenticatedAccount(data.data);

            window.location = '/';
          }

          /**
           * @name loginErrorFn
           * @desc Log "Epic failure!" to the console
           */
          function loginErrorFn(data, status, headers, config) {
            vm.error = data.data.message;
          }
        }
    }


})();