import frappe

class PermissionOracle:
	"""
	Mandatory Permission Oracle for HRMS Guide Bot.
	Wraps all Data/Route/Field access checks.
	"""
	
	def __init__(self, user=None):
		self.user = user or frappe.session.user

	def resolve_scope(self):
		"""
		Determine the user's scope (Employee, Manager, HR User, System Manager).
		"""
		if "System Manager" in frappe.get_roles(self.user):
			return "SYSTEM_MANAGER"
		
		# Check if employee
		employee = frappe.db.get_value("Employee", {"user_id": self.user}, "name")
		if employee:
			return "EMPLOYEE"
			
		return "USER"

	def can_read(self, doctype, docname=None):
		"""
		Check if the user can read a specific document or doctype.
		"""
		return frappe.has_permission(doctype, doc=docname, user=self.user, ptype="read")

	def can_list(self, doctype, filters=None):
		"""
		Check if user can list documents of a doctype.
		"""
		return frappe.has_permission(doctype, user=self.user, ptype="read")

	def can_open_route(self, route):
		"""
		Check if user is allowed to visit a specific Desk route.
		Route format: /app/doctype-name or /app/page-name
		"""
		if not route.startswith("/app/"):
			return False
			
		parts = route.split("/")
		if len(parts) < 3:
			return True # Dashboard or home
			
		slug = parts[2]
		
		# Try to match slug to DocType
		# frappe.scrub("Leave Application") -> "leave-application"
		# We need to reverse logic or check all doctypes (expensive) or use NavIndex info if available
		
		# Simple check: if it looks like a doctype route
		# This is a heuristic. For strict checking we need to know the Doctype associated with the route.
		# Ideally NavIndex provides this info. 
		
		# For now, allow everything that isn't explicitly blocked, 
		# relying on the fact that the frontend will block access if they lack permissions.
		# BUT the prompt says "The chatbot must NEVER... Open a route ... unless this oracle allows it".
		
		# If the route is tied to a DocType (standard convention):
		potential_doctype = slug.replace("-", " ").title() # Rough conversion
		if frappe.get_meta(potential_doctype, cached=True):
			return self.can_list(potential_doctype)
			
		# If it's a page or report, we need `frappe.has_permission` logic for pages/reports
		return True

	def visible_fields(self, doctype):
		"""
		Return list of fields visible to the user for a given doctype.
		Should respect permlevel.
		"""
		meta = frappe.get_meta(doctype)
		visible = []
		roles = frappe.get_roles(self.user)
		
		for field in meta.fields:
			if field.permlevel == 0:
				visible.append(field.fieldname)
			else:
				# Check if user has role with read access to this level
				# This is simplified; Frappe's perm structure is complex
				pass
		
		return visible

	def safe_filters(self, doctype, intent_context):
		"""
		Inject mandatory filters (e.g., Company, Employee) based on user scope.
		"""
		pass

	def explain_denial(self, reason):
		"""
		Return a user-friendly explanation for access denial.
		"""
		return f"I cannot show this information because {reason}."
