from frappe import _

def get_data():
	return [
		{
			"label": _("HRMS Guide Bot"),
			"icon": "robot",
			"items": [
				{
					"type": "doctype",
					"name": "NavIndex",
					"label": _("Nav Index"),
				},
				{
					"type": "doctype",
					"name": "PolicyDocument",
					"label": _("Policy Document"),
				},
                {
					"type": "doctype",
					"name": "BotTelemetry",
					"label": _("Bot Telemetry"),
				},
                {
					"type": "doctype",
					"name": "EscalationMatrix",
					"label": _("Escalation Matrix"),
				},
			]
		}
	]
