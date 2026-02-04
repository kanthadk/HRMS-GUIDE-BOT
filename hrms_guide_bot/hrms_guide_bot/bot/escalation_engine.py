import frappe
from hrms_guide_bot.hrms_guide_bot.doctype.bottelemetry.bottelemetry import log_event

class EscalationEngine:
	def __init__(self, user=None):
		self.user = user or frappe.session.user

	def resolve(self, query, context=None):
		"""
		Handle escalation requests.
		"""
		# 1. Identify Intent/Team from query (Mock Classifier)
		# "Report payroll issue" -> Payroll
		# "IT help" -> IT
		
		team = "HR" # Default
		if "payroll" in query.lower():
			team = "Payroll"
		elif "it" in query.lower():
			team = "IT"
			
		# 2. Get Escalation Matrix Config
		matrix = frappe.db.get_value("EscalationMatrix", {"team": team, "ticket_type": "Issue"}, ["name", "required_fields", "redaction_fields", "sla_hours"], as_dict=True)
		
		if not matrix:
			return {
				"message": "I cannot find an escalation path for this request. Please contact HR manually."
			}
			
		# 3. Check if we have required fields
		# If context has 'missing_info', we might be in a slot-filling loop.
		# For V1, assume we just open the ticket form or return a link.
		
		# 4. Create Ticket (Stub)
		# ticket = frappe.new_doc("Issue") ...
		
		# 5. Return Response
		return {
			"message": f"I can escalate this to the {team} team. Expected resolution within {matrix.sla_hours} hours. Please confirm to proceed.",
			"action": {
				"type": "CREATE_TICKET", # Frontend will handle confirmation
				"team": team,
				"matrix": matrix.name
			}
		}

	def create_ticket(self, matrix_name, description):
		"""
		Actual ticket creation logic (called after confirmation).
		"""
		matrix = frappe.get_doc("EscalationMatrix", matrix_name)
		
		# Redaction logic (Stub)
		# description = redact(description, matrix.redaction_fields)
		
		ticket = frappe.get_doc({
			"doctype": "Issue",
			"subject": f"Bot Escalation: {matrix.team}",
			"description": description,
			"raised_by": self.user
		})
		ticket.insert(ignore_permissions=True)
		
		log_event("ticket_created", self.user, {"ticket": ticket.name, "team": matrix.team})
		
		return ticket.name
