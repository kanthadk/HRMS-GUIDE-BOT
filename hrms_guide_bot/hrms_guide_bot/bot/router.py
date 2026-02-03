import frappe
from hrms_guide_bot.hrms_guide_bot.bot.nav_engine import NavEngine

def route_query(message, context=None):
	"""
	Route the user's message to the appropriate intent handler.
	"""
	message = message.lower().strip()
	
	intent = detect_intent(message)
	confidence = 1.0 # Placeholder
	
	payload = {}
	
	if intent == "NAVIGATION":
		engine = NavEngine()
		payload = engine.resolve(message)
	elif intent == "POLICY":
		from hrms_guide_bot.hrms_guide_bot.bot.policy_engine import PolicyEngine
		engine = PolicyEngine()
		payload = engine.resolve(message)
	elif intent == "STATUS":
		from hrms_guide_bot.hrms_guide_bot.bot.status_engine import StatusEngine
		payload = StatusEngine().resolve(message)
	elif intent == "MANAGER_DAILY":
		from hrms_guide_bot.hrms_guide_bot.bot.manager_daily import get_manager_daily_briefing
		payload = {"actions": get_manager_daily_briefing()}
	elif intent == "ESCALATION":
		from hrms_guide_bot.hrms_guide_bot.bot.escalation_engine import EscalationEngine
		payload = EscalationEngine().resolve(message)
	else:
		payload = {
			"message": "I didn't understand that. Try 'Go to Leave Application' or 'Leave Policy'."
		}

	return {
		"intent": intent,
		"confidence": confidence,
		"payload": payload
	}

def detect_intent(message):
	"""
	Simple rule-based intent detection.
	"""
	nav_keywords = ["go to", "open", "show me", "list", "create", "new"]
	policy_keywords = ["policy", "rule", "how-to", "how do i", "explain"]
	status_keywords = ["status", "where is", "check", "approved"]
	manager_keywords = ["what should i do", "my tasks", "approvals", "pending"]
	
	for kw in nav_keywords:
		if message.startswith(kw):
			return "NAVIGATION"
			
	for kw in policy_keywords:
		if kw in message:
			return "POLICY"
			
	for kw in status_keywords:
		if kw in message:
			return "STATUS"

	for kw in manager_keywords:
		if kw in message:
			return "MANAGER_DAILY"
			
	if "escalate" in message or "complaint" in message:
		return "ESCALATION"
			
	# Default fallback (could be clarification)
	return "UNKNOWN"
