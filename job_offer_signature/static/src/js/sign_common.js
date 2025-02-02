odoo.define('job_offer_signature.document_signing', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var config = require('web.config');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Document = require('sign.Document');
    var NameAndSignature = require('web.name_and_signature').NameAndSignature;
    var PDFIframe = require('sign.PDFIframe');
    var session = require('web.session');
    var Widget = require('web.Widget');
    var sign = require('sign.document_signing');

    var _t = core._t;
    sign.SignableDocument.include({

       events: {
          'click .o_sign_reject button': 'RejectItemDocument',
       },
       RejectItemDocument: function(e) {
         var self = this;
         self._rpc({
                route: '/offer/reject/' + this.requestID
            })
            .then(function(response) {
               document.location.pathname = '/offer/reject/thank_you/';
            });
       },
    });
});