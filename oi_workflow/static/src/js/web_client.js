odoo.define('web.client.oi_workflow', function(require) {
"use strict";

	var core = require('web.core');
	var rpc = require("web.rpc");
	
	core.bus.on("web_client_ready", null, function () {

		rpc.query({
			route : '/oi_workflow/approval_settings'
		}).then(function (data) {
			core.approval_models = data.approval_models;
			core.disable_edit_on_non_approval = data.disable_edit_on_non_approval
			core.state_models = data.state_models;
		});
			
	});
	
		
});