import frappe
from hrms_guide_bot.hrms_guide_bot.permission_oracle import PermissionOracle

class StatusEngine:
	def __init__(self, user=None):
		self.user = user or frappe.session.user
		self.oracle = PermissionOracle(self.user)

	def resolve(self, query):
		"""
		Check status of user's requests (Leave, Expense, etc.)
		"""
		# Simple regex or keyword matching to identify DocType
		
		# Example: "Status of my leave"
		doctype = None
		if "leave" in query:
			doctype = "Leave Application"
		elif "expense" in query:
			doctype = "Expense Claim"
		elif "loan" in query:
			doctype = "Loan Application"
		# Add more mappings
		
		if not doctype:
			return {
				"message": "I'm not sure which application status you are asking for. Try 'status of my leave'."
			}

		# Check permissions
		if not self.oracle.can_list(doctype):
			return {"message": "You don't have permission to view these records."}
			
		# Fetch latest records
		# Assuming standard 'employee' field or 'owner'
		filters = {"owner": self.user}
		if frappe.get_meta(doctype).has_field("employee"):
			employee = frappe.db.get_value("Employee", {"user_id": self.user}, "name")
			if employee:
				filters = {"employee": employee}
		
		records = frappe.get_all(doctype, 
			filters=filters,
			fields=["name", "status", "modified"],
			order_by="modified desc",
			limit=3
		)
		
		if not records:
			return {"message": f"You have no recent {doctype} records."}
			
		from hrms_guide_bot.hrms_guide_bot.doctype.bottelemetry.bottelemetry import log_event
		log_event("intent_detected", self.user, {"intent": "STATUS", "doctype": doctype})
			
		return {
			"records": records,
			"doctype": doctype
		}
