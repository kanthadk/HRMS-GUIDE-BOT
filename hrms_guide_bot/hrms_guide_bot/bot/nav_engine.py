import frappe
from hrms_guide_bot.hrms_guide_bot.permission_oracle import PermissionOracle

class NavEngine:
	def __init__(self, user=None):
		self.user = user or frappe.session.user
		self.oracle = PermissionOracle(self.user)

	def resolve(self, query):
		"""
		Resolve a navigation query to a route.
		"""
		# 1. Search NavIndex (Full text or fuzzy - using SQL LIKE for now)
		results = frappe.db.get_all("NavIndex", 
			filters={
				"label": ["like", f"%{query}%"]
			},
			fields=["label", "route", "type", "required_roles", "popularity_score"],
			limit=5,
			order_by="popularity_score desc"
		)

		if not results:
			# Fallback: Check synonyms (this is expensive in SQL, ideally use dedicated search index)
			# For now, return empty or try to guess standard DocTypes
			pass

		# 2. Filter by Permissions
		allowed_results = []
		for item in results:
			# Check role-based access defined in NavIndex
			if item.required_roles:
				# TODO: parse item.required_roles json and check against user roles
				pass
			
			# Check global permission oracle
			if self.oracle.can_open_route(item.route):
				allowed_results.append({
					"label": item.label,
					"route": item.route,
					"type": item.type
				})

		if allowed_results:
			# match found
			top_match = allowed_results[0]
			
			from hrms_guide_bot.hrms_guide_bot.doctype.bot_telemetry.bot_telemetry import log_event
			log_event("nav_shown", self.user, {"query": query, "route": top_match["route"]})

			return {
				"path": [top_match["route"]],
				"open_url": top_match["route"], # Front-end will route.push this
				"alt_suggestions": allowed_results[1:],
				"required_role": None
			}

		return {
			"path": [],
			"open_url": None,
			"alt_suggestions": [],
			"message": "I couldn't find a page matching that description."
		}
