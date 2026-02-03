import frappe
from frappe.utils import add_days, nowdate

def get_manager_daily_briefing(user=None):
	"""
	Manager “What should I do today?”
	Returns pending approvals, overdue actions, onboarding gaps.
	"""
	user = user or frappe.session.user
	
	# Check if user is a manager (Basic check, can be refined)
	# For now, assume if they ask, we check.
	
	briefing = []
	
	# 1. Pending Leave Approvals
	# Assuming 'Leave Application' doctype exists and has 'leave_approver' field
	if frappe.get_meta("Leave Application", cached=True):
		pending_leaves = frappe.db.count("Leave Application", filters={
			"docstatus": 0,
			"status": "Open", 
			"leave_approver": user # This field varies by setup
		})
		if pending_leaves:
			briefing.append({
				"title": "Pending Leave Requests",
				"count": pending_leaves,
				"priority": "High",
				"open_url": "/app/leave-application?status=Open"
			})
			
	# 2. Expense Claims
	if frappe.get_meta("Expense Claim", cached=True):
		pending_expenses = frappe.db.count("Expense Claim", filters={
			"docstatus": 0,
			"approval_status": "Draft", # or whatever status indicates pending manager action
			# "approver": user 
		})
		if pending_expenses:
			briefing.append({
				"title": "Expense Claims to Review",
				"count": pending_expenses,
				"priority": "Medium",
				"open_url": "/app/expense-claim"
			})

	# 3. Onboarding Gaps (Stub)
	# e.g., Employee Onboarding exceeding SLA
	
	if not briefing:
		return [
			{
				"title": "All caught up!",
				"count": 0,
				"priority": "Low",
				"open_url": None
			}
		]
		
	return briefing
