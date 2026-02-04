# Copyright (c) 2024, Surendhar Nadh Cherukuri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BotTelemetry(Document):
	pass

def log_event(event_type, user, payload=None, latency_ms=None):
	"""
	Quickly log a telemetry event.
	Ideally this should be deferred/backgrounded to avoid blocking the user.
	"""
	doc = frappe.get_doc({
		"doctype": "BotTelemetry",
		"event_type": event_type,
		"user": user,
		"payload": frappe.as_json(payload) if payload else None,
		"latency_ms": latency_ms
	})
	doc.insert(ignore_permissions=True)
