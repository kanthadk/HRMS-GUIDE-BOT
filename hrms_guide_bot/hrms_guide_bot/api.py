import frappe
from frappe import _

@frappe.whitelist()
def chat(message=None, context=None):
	"""
	Single API Entrypoint for HRMS Guide Bot.
	
	Expected Input:
	- message: User's query string
	- context: Optional JSON object with current route, selections, etc.
	
	Returns JSON:
	{
		intent: "NAVIGATION" | "POLICY" | "STATUS" | "ERROR",
		confidence: float,
		payload: dict
	}
	"""
	if not message:
		return {
			"intent": "ERROR",
			"confidence": 1.0,
			"payload": {
				"reason_type": "SYSTEM_BLOCK",
				"message": _("Empty message received.")
			}
		}

	from hrms_guide_bot.hrms_guide_bot.bot.router import route_query
	return route_query(message, context)
