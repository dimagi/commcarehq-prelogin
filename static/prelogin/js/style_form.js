var styleContactForm = function ($form, conf) {
    'use strict';
    $form.find('.actions').addClass('form-actions')
        .append('<div class="col-sm-offset-4 controls col-sm-8"/>');
    $form.find('input[type="submit"]').detach().appendTo($form.find('.form-actions .controls'));
    $form.find('.hs-form-field').addClass('form-group')
        .find('label').addClass('control-label col-sm-4');
    $form.find('.input').addClass('controls col-sm-8');
    $form.find('textarea').attr('rows', '10');
};

var endContactForm = function ($form, conf, e) {
    var $closeBtn = $('<div class="form-actions" />]')
        .append($('<button type="button" class="btn btn-default" />').text("Close"));
    $('.hbspot-form .submitted-message').after($closeBtn);
};
