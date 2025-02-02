odoo.define('archer_portal.job_offer', function (require) {
        "use strict";
        var rpc = require('web.rpc')
        var publicWidget = require('web.public.widget');
        var time = require('web.time');
        const session = require('web.session');

        publicWidget.registry.PortalWebsite = publicWidget.Widget.extend({
            selector: '.job_offer_footer',
            events: {
                'click .job_offer_accept': 'accept_job_offer',
            },


            accept_job_offer: function (ev) {
               alert('sss')
            }


        });

    }
);
