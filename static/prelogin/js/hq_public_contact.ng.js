(function (angular, undefined) {
    'use strict';
    // module: hq.public.contact
    var contact = angular.module('hq.public.contact', [
        'ngResource',
        'ngRoute',
        'ng.django.rmi'
    ]);

    var contactControllers = {};
    contactControllers.contactFormValidationController = function ($scope, djangoRMI) {
        $scope.master = {};
        var self = {};

        self.showSuccessMessage = function (resp) {
            // hide modal
            $('#contactDimagi').modal('hide');
            // reset form
            $('#contact-dimagi-form')[0].reset();
            // show success modal
            $('#thanksForContactingUs').modal('show');
        };

        self.showErrorMessage = function () {
            $('#contactUsFormIssues').modal('show');
        };

        $scope.send_email = function(contact) {
            $scope.master = angular.copy(contact);
            djangoRMI.send_email(contact).success(
                self.showSuccessMessage
            ).error(self.showErrorMessage);
        };

        $scope.reset = function() {
            $scope.contact = angular.copy($scope.master);
        };

        $scope.reset();
    };
    contact.controller(contactControllers);

}(window.angular));
