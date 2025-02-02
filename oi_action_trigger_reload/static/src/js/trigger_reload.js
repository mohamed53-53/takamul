odoo.define('oi_action_trigger_reload', function(require) {
	"use strict";

	var core = require('web.core');

	var TriggerReload = function(parent, action) {

		if (parent && parent.services && parent.services.action) {
			const controller = parent.services.action.currentController;
			const state = controller.getLocalState();
			state.__legacy_widget__.reload().then(function(){
				document.body.click();
			})
			
		}
		
		return {
			type: 'ir.actions.act_window_close'
		}
	}

	core.action_registry.add('trigger_reload', TriggerReload);

});